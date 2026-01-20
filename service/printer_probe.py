# printer_probe.py
# Win32 Print Spooler queries for printer status


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
if sys.platform == 'win32':
	import printer_probe_win32
	get_printer_job_count = printer_probe_win32.get_printer_job_count
	is_printer_available = printer_probe_win32.is_printer_available
else:
	def get_printer_job_count(printer_name):
		raise NotImplementedError("Printer monitoring only supported on Windows.")
	def is_printer_available(printer_name, job_threshold):
		raise NotImplementedError("Printer monitoring only supported on Windows.")

