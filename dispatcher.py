# dispatcher.py
# Core dispatcher logic for polling, file selection, atomic claiming, and dispatch
import os
import time
import shutil
import threading

class Dispatcher:
    def __init__(self, config, printer_adapter, log_callback=None):
        self.config = config
        self.printer_adapter = printer_adapter
        self.log_callback = log_callback
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None

    def run(self):
        while self.running:
            try:
                if self.printer_adapter.is_printer_idle(self.config['spooler_job_threshold']):
                    file_path = self._select_eligible_file()
                    if file_path:
                        self._claim_and_dispatch(file_path)
                time.sleep(self.config['polling_interval'])
            except Exception as e:
                self._log(f"[ERROR] Dispatcher error: {e}")
                time.sleep(5)

    def _select_eligible_file(self):
        folder = self.config['master_folder_path']
        exts = [e.strip().lower() for e in self.config['allowed_file_extensions'].split(',')]
        min_age = self.config['minimum_file_age']
        now = time.time()
        candidates = []
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if not os.path.isfile(fpath):
                continue
            if not any(fname.lower().endswith(f'.{ext}') for ext in exts):
                continue
            if now - os.path.getmtime(fpath) < min_age:
                continue
            candidates.append((os.path.getmtime(fpath), fpath))
        if not candidates:
            return None
        candidates.sort()
        return candidates[0][1]

    def _claim_and_dispatch(self, src):
        hot_folder = self.config['printer_hot_folder_path']
        dst = os.path.join(hot_folder, os.path.basename(src))
        try:
            # Try atomic move (same volume)
            os.replace(src, dst)
            self._log(f"[INFO] Job claimed and dispatched: {src} -> {dst}")
        except OSError:
            # Cross-volume: copy, verify, delete
            shutil.copy2(src, dst)
            if os.path.getsize(src) == os.path.getsize(dst):
                os.remove(src)
                self._log(f"[INFO] Job claimed and dispatched (copy): {src} -> {dst}")
            else:
                os.remove(dst)
                self._log(f"[ERROR] File copy verification failed: {src}")

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
