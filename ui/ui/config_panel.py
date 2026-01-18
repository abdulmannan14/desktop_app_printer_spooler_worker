# Configuration Panel UI (stub)

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt
import os
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config_utils

class ConfigPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self.load_config()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        # Fields
        self.printer_name = QLineEdit()
        self.master_folder_path = QLineEdit()
        self.printer_hot_folder_path = QLineEdit()
        self.allowed_file_extensions = QLineEdit()
        self.spooler_job_threshold = QSpinBox()
        self.spooler_job_threshold.setMinimum(1)
        self.spooler_job_threshold.setMaximum(1000)
        self.polling_interval = QSpinBox()
        self.polling_interval.setMinimum(1)
        self.polling_interval.setMaximum(3600)
        self.minimum_file_age = QSpinBox()
        self.minimum_file_age.setMinimum(0)
        self.minimum_file_age.setMaximum(86400)
        self.log_file_path = QLineEdit()

        # Add fields to form
        form.addRow("Printer Name / ID:", self.printer_name)
        form.addRow("Master Folder Path:", self.master_folder_path)
        form.addRow("Printer Hot Folder Path:", self.printer_hot_folder_path)
        form.addRow("Allowed File Extensions:", self.allowed_file_extensions)
        form.addRow("Spooler Job Threshold:", self.spooler_job_threshold)
        form.addRow("Polling Interval (seconds):", self.polling_interval)
        form.addRow("Minimum File Age (seconds):", self.minimum_file_age)
        form.addRow("Log File Path:", self.log_file_path)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Config")
        self.reload_btn = QPushButton("Reload Config")
        self.test_btn = QPushButton("Test Paths (Mock)")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.reload_btn)
        btn_layout.addWidget(self.test_btn)
        layout.addLayout(btn_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #007700; font-weight: bold;")
        layout.addWidget(self.status_label)

        # Connect buttons
        self.save_btn.clicked.connect(self.save_config)
        self.reload_btn.clicked.connect(self.load_config)
        self.test_btn.clicked.connect(self.test_paths)

        layout.addStretch()

    def load_config(self):
        config = config_utils.load_config()
        self.printer_name.setText(config.get("printer_name", ""))
        self.master_folder_path.setText(config.get("master_folder_path", ""))
        self.printer_hot_folder_path.setText(config.get("printer_hot_folder_path", ""))
        self.allowed_file_extensions.setText(config.get("allowed_file_extensions", ""))
        self.spooler_job_threshold.setValue(config.get("spooler_job_threshold", 1))
        self.polling_interval.setValue(config.get("polling_interval", 10))
        self.minimum_file_age.setValue(config.get("minimum_file_age", 30))
        self.log_file_path.setText(config.get("log_file_path", ""))
        self.status_label.setText("Config loaded.")

    def save_config(self):
        config = self._gather_config()
        if not self._validate_config(config):
            return
        config_utils.save_config(config)
        self.status_label.setText("Config saved.")

    def test_paths(self):
        # Mock test: just check if paths are non-empty and look like paths
        master = self.master_folder_path.text().strip()
        hot = self.printer_hot_folder_path.text().strip()
        log = self.log_file_path.text().strip()
        if all([master, hot, log]):
            self.status_label.setText("Paths test: Success (mocked)")
        else:
            self.status_label.setText("Paths test: Failed (mocked)")

    def _gather_config(self):
        return {
            "printer_name": self.printer_name.text().strip(),
            "master_folder_path": self.master_folder_path.text().strip(),
            "printer_hot_folder_path": self.printer_hot_folder_path.text().strip(),
            "allowed_file_extensions": self.allowed_file_extensions.text().strip(),
            "spooler_job_threshold": self.spooler_job_threshold.value(),
            "polling_interval": self.polling_interval.value(),
            "minimum_file_age": self.minimum_file_age.value(),
            "log_file_path": self.log_file_path.text().strip(),
        }

    def _validate_config(self, config):
        # Basic validation
        if not config["printer_name"]:
            self._show_error("Printer Name is required.")
            return False
        if not config["master_folder_path"]:
            self._show_error("Master Folder Path is required.")
            return False
        if not config["printer_hot_folder_path"]:
            self._show_error("Printer Hot Folder Path is required.")
            return False
        if not re.match(r"^[\w, ]+$", config["allowed_file_extensions"]):
            self._show_error("Allowed File Extensions must be comma-separated (e.g. pdf,txt)")
            return False
        if not config["log_file_path"]:
            self._show_error("Log File Path is required.")
            return False
        return True

    def _show_error(self, message):
        QMessageBox.critical(self, "Validation Error", message)
        self.status_label.setText(f"Error: {message}")
