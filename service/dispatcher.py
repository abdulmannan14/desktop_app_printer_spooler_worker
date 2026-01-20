# dispatcher.py
# Job selection & claiming logic for Windows Service



import os
import sys
import time
import logging
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui import config_utils
from printer_probe import is_printer_available
from file_ops import atomic_claim_file, atomic_rename

def run_service_loop():
	config = config_utils.load_config()
	printer_name = config["printer_name"]
	master_folder = config["master_folder_path"]
	hot_folder = config["printer_hot_folder_path"]
	allowed_exts = [e.strip().lower() for e in config["allowed_file_extensions"].split(",")]
	job_threshold = config["spooler_job_threshold"]
	poll_interval = config["polling_interval"]
	min_file_age = config["minimum_file_age"]
	log_path = config["log_file_path"]


	print(f"[DEBUG] Logging to: {log_path}")
	logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
	logging.info(f"Service started. Monitoring folder: {master_folder}")
	print("[DEBUG] Service started")

	permanent_failures = set()

	print(f"[DEBUG] Dispatcher loop starting... Monitoring folder: {master_folder}")
	while True:
		try:
			print("[DEBUG] Loop iteration start")
			# 1. Check printer availability
			if not is_printer_available(printer_name, job_threshold):
				print(f"[DEBUG] Printer busy or unavailable: {printer_name}")
				logging.info(f"Printer busy or unavailable: {printer_name}")
				time.sleep(poll_interval)
				continue

			# 2. Scan master folder for eligible files
			candidates = []
			now = time.time()
			try:
				files = os.listdir(master_folder)
				now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				print(f"[DEBUG] {now_str} | Scanning folder: {master_folder} | Files: {files}")
				logging.info(f"Scanning folder: {master_folder} | Files: {files}")
			except Exception as e:
				now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				print(f"[DEBUG] {now_str} | Failed to list master folder: {e}")
				logging.error(f"Failed to list master folder: {e}")
				time.sleep(poll_interval)
				continue
			for fname in files:
				fpath = os.path.join(master_folder, fname)
				if not os.path.isfile(fpath):
					continue
				ext = os.path.splitext(fname)[1][1:].lower()
				if ext not in allowed_exts:
					continue
				age = now - os.path.getmtime(fpath)
				if age < min_file_age:
					continue
				if fpath in permanent_failures:
					continue
				candidates.append((age, fpath))
			candidates.sort()

			# 3. Try to claim and dispatch the oldest eligible file
			claimed = False
			for _, fpath in candidates:
				base = os.path.basename(fpath)
				claim_name = f"{os.path.splitext(base)[0]}.claimed.{printer_name}"
				claim_path = os.path.join(master_folder, claim_name)
				print(f"[DEBUG] Attempting to claim: {base}")
				try:
					if atomic_claim_file(fpath, claim_path, printer_name):
						print(f"[DEBUG] Job claimed: {base}")
						logging.info(f"Job claimed: {base}")
						# 4. Move to hot folder atomically
						hot_path = os.path.join(hot_folder, base)
						try:
							atomic_rename(claim_path, hot_path)
							print(f"[DEBUG] Job dispatched: {base}")
							logging.info(f"Job dispatched: {base}")
						except Exception as e:
							print(f"[DEBUG] Failed to dispatch job to hot folder: {base}, error: {e}")
							logging.error(f"Failed to dispatch job to hot folder: {base}, error: {e}")
							permanent_failures.add(fpath)
						claimed = True
						break
					else:
						print(f"[DEBUG] Failed to claim: {base}")
						logging.warning(f"Failed to claim: {base}")
				except Exception as e:
					print(f"[DEBUG] Permanent failure claiming {base}: {e}")
					logging.error(f"Permanent failure claiming {base}: {e}")
					permanent_failures.add(fpath)

			if not claimed:
				print("[DEBUG] No file claimed this iteration.")
				time.sleep(poll_interval)
		except Exception as e:
			print(f"[DEBUG] Service error: {e}")
			logging.error(f"Service error: {e}")
			time.sleep(poll_interval)

if __name__ == "__main__":
	print("[DEBUG] dispatcher.py running as script. Starting service loop...")
	run_service_loop()

