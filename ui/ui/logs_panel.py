# Logs Panel UI (stub)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config_utils

class LogsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.load_logs()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        filter_layout = QHBoxLayout()
        self.info_btn = QPushButton("INFO")
        self.warn_btn = QPushButton("WARNING")
        self.error_btn = QPushButton("ERROR")
        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.info_btn)
        filter_layout.addWidget(self.warn_btn)
        filter_layout.addWidget(self.error_btn)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        self.info_btn.clicked.connect(lambda: self.load_logs("INFO"))
        self.warn_btn.clicked.connect(lambda: self.load_logs("WARNING"))
        self.error_btn.clicked.connect(lambda: self.load_logs("ERROR"))

    def load_logs(self, level=None):
        config = config_utils.load_config()
        log_path = config.get("log_file_path", "printer_service.log")
        # For Phase 1, mock log content
        logs = [
            "2026-01-18 10:00:00 [INFO] Service started",
            "2026-01-18 10:01:00 [INFO] Job claimed: file1.pdf",
            "2026-01-18 10:02:00 [WARNING] Printer slow response",
            "2026-01-18 10:03:00 [ERROR] Failed to move file2.pdf",
            "2026-01-18 10:04:00 [INFO] Job dispatched: file1.pdf",
        ]
        if level:
            logs = [l for l in logs if f"[{level}]" in l]
        self.log_view.setPlainText("\n".join(logs))
