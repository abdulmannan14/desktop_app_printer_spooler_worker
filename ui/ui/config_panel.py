from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QSpinBox, QStyle, QInputDialog
)
from PySide6.QtCore import Qt
import os
import re
import sys
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
        self.printer_select_btn = QPushButton()
        self.printer_select_btn.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.printer_select_btn.setToolTip("Select Printer")
        self.printer_select_btn.setFixedWidth(32)
        self.master_folder_path = QLineEdit()
        self.master_folder_btn = QPushButton()
        self.master_folder_btn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.master_folder_btn.setToolTip("Select Master Folder")
        self.master_folder_btn.setFixedWidth(32)

        self.printer_hot_folder_path = QLineEdit()
        self.printer_hot_folder_btn = QPushButton()
        self.printer_hot_folder_btn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.printer_hot_folder_btn.setToolTip("Select Printer Hot Folder")
        self.printer_hot_folder_btn.setFixedWidth(32)
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
        self.log_file_btn = QPushButton()
        self.log_file_btn.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.log_file_btn.setToolTip("Select Log File")
        self.log_file_btn.setFixedWidth(32)

        # Add fields to form
        printer_layout = QHBoxLayout()
        printer_layout.addWidget(self.printer_name)
        printer_layout.addWidget(self.printer_select_btn)
        form.addRow("Printer Name / ID:", printer_layout)
        master_folder_layout = QHBoxLayout()
        master_folder_layout.addWidget(self.master_folder_path)
        master_folder_layout.addWidget(self.master_folder_btn)
        form.addRow("Master Folder Path:", master_folder_layout)

        hot_folder_layout = QHBoxLayout()
        hot_folder_layout.addWidget(self.printer_hot_folder_path)
        hot_folder_layout.addWidget(self.printer_hot_folder_btn)
        form.addRow("Printer Hot Folder Path:", hot_folder_layout)
        form.addRow("Allowed File Extensions:", self.allowed_file_extensions)
        form.addRow("Spooler Job Threshold:", self.spooler_job_threshold)
        form.addRow("Polling Interval (seconds):", self.polling_interval)
        form.addRow("Minimum File Age (seconds):", self.minimum_file_age)
        log_file_layout = QHBoxLayout()
        log_file_layout.addWidget(self.log_file_path)
        log_file_layout.addWidget(self.log_file_btn)
        form.addRow("Log File Path:", log_file_layout)

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
        self.master_folder_btn.clicked.connect(self._select_master_folder)
        self.printer_hot_folder_btn.clicked.connect(self._select_hot_folder)
        self.log_file_btn.clicked.connect(self._select_log_file)
        self.printer_select_btn.clicked.connect(self._select_printer)

    def _select_printer(self):
        # Get available printers using Windows PowerShell
        import subprocess
        try:
            result = subprocess.run([
                "powershell", "-Command", "Get-Printer | Select-Object -ExpandProperty Name"
            ], capture_output=True, text=True, timeout=5)
            printers = [p.strip() for p in result.stdout.splitlines() if p.strip()]
        except Exception as e:
            printers = []
        if not printers:
            printers = [self.printer_name.text() or "No printers found"]
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getItem(self, "Select Printer", "Available printers:", printers, editable=False)
        if ok and name:
            self.printer_name.setText(name)
    def _select_master_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Master Folder", "")
        if folder:
            self.master_folder_path.setText(folder)

    def _select_hot_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Printer Hot Folder", "")
        if folder:
            self.printer_hot_folder_path.setText(folder)

    def _select_log_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Select Log File", "", "Log Files (*.log);;All Files (*)")
        if file:
            self.log_file_path.setText(file)

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
        self.status_label.setText("Config saved. Restarting dispatcher...")
        # Restart dispatcher.py process (script mode)
        try:
            import psutil
            import subprocess
            import time
            # Find and terminate all dispatcher.py processes
            killed = False
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'dispatcher.py' in ' '.join(p.info['cmdline']):
                        p.terminate()
                        killed = True
                except Exception:
                    continue
            if killed:
                time.sleep(1)  # Give time to terminate
            # Start dispatcher.py again
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            dispatcher_path = os.path.join(project_root, 'service', 'dispatcher.py')
            python_exe = sys.executable
            subprocess.Popen([python_exe, dispatcher_path], cwd=project_root)
            self.status_label.setText("Config saved and dispatcher restarted.")
        except Exception as e:
            self.status_label.setText(f"Config saved, but failed to restart dispatcher: {e}")

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
