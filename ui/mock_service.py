# Mock service loop for Phase 1
# This is a placeholder for the simulated backend logic
import threading
import time

class MockService:
    def __init__(self, config_loader, status_callback=None):
        self._running = False
        self._thread = None
        self.config_loader = config_loader
        self.status_callback = status_callback
        self._job_count = 0
        self._last_dispatched = None
        self._last_error = None

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None

    def _run(self):
        while self._running:
            # Simulate job dispatch
            self._job_count = 0
            self._last_dispatched = time.strftime("%Y-%m-%d %H:%M:%S")
            self._last_error = None
            if self.status_callback:
                self.status_callback(self.status())
            time.sleep(self.config_loader().get("polling_interval", 10))

    def status(self):
        return {
            "job_count": self._job_count,
            "last_dispatched": self._last_dispatched,
            "last_error": self._last_error,
        }
