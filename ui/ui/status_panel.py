# Status / Monitoring Panel UI (stub)

from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer

class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.refresh_status()
        # Auto-refresh every 3 seconds
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh_status)
        self._timer.start(3000)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.service_status = QLabel()
        self.printer_status = QLabel()
        self.job_count = QLabel()
        self.last_dispatched = QLabel()
        self.last_error = QLabel()

        form.addRow("Service Status:", self.service_status)
        form.addRow("Printer Status:", self.printer_status)
        form.addRow("Current Spooler Job Count:", self.job_count)
        form.addRow("Last Dispatched Job:", self.last_dispatched)
        form.addRow("Last Error:", self.last_error)

        layout.addLayout(form)
        layout.addStretch()

        # Refresh button for real status
        self.refresh_btn = QPushButton("Refresh Status")
        self.refresh_btn.clicked.connect(self.refresh_status)
        layout.addWidget(self.refresh_btn)

        # Stop dispatcher button
        self.stop_dispatcher_btn = QPushButton("Stop Dispatcher")
        self.stop_dispatcher_btn.clicked.connect(self.stop_dispatcher)
        layout.addWidget(self.stop_dispatcher_btn)
    def stop_dispatcher(self):
        import psutil
        killed = False
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'dispatcher.py' in ' '.join(p.info['cmdline']):
                    p.terminate()
                    killed = True
            except Exception:
                continue
        if killed:
            self.service_status.setText("Stopped (by user)")
        else:
            self.service_status.setText("Dispatcher not running")

    def refresh_status(self):
        import os
        import sys
        import datetime
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        import config_utils
        import service.printer_probe as printer_probe

        config = config_utils.load_config()
        printer_name = config.get("printer_name", "")
        log_path = config.get("log_file_path", "printer_service.log")

        # Service status: check if dispatcher is running (simple check)
        import psutil
        service_running = False
        for p in psutil.process_iter(['name', 'cmdline']):
            try:
                if 'dispatcher.py' in ' '.join(p.info['cmdline']):
                    service_running = True
                    break
            except Exception:
                continue
        self.service_status.setText("Running" if service_running else "Stopped")

        # Printer status and job count
        try:
            job_count = printer_probe.get_printer_job_count(printer_name)
            self.job_count.setText(str(job_count) if job_count >= 0 else "Unknown")
            if job_count == 0:
                self.printer_status.setText("Idle")
            elif job_count > 0:
                self.printer_status.setText("Busy")
            else:
                self.printer_status.setText("Unknown")
        except Exception as e:
            self.printer_status.setText(f"Error: {e}")
            self.job_count.setText("Unknown")

        # Last dispatched job and last error from log file
        last_dispatched = ""
        last_error = ""
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "Job dispatched:" in line:
                        last_dispatched = line.strip()
                    if "ERROR" in line:
                        last_error = line.strip()
        self.last_dispatched.setText(last_dispatched)
        self.last_error.setText(last_error)
