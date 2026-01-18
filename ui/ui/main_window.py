# Main window for Printer Automation UI

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from .config_panel import ConfigPanel
from .status_panel import StatusPanel
from .logs_panel import LogsPanel
from .control_panel import ControlPanel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mock_service import MockService
import config_utils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Printer Automation Service")
        self.setMinimumSize(900, 600)
        self._init_ui()

    def _init_ui(self):
        self.tabs = QTabWidget()
        self.config_panel = ConfigPanel()
        self.status_panel = StatusPanel()
        self.logs_panel = LogsPanel()
        self.control_panel = ControlPanel()

        self.tabs.addTab(self.config_panel, "Configuration")
        self.tabs.addTab(self.status_panel, "Status / Monitoring")
        self.tabs.addTab(self.logs_panel, "Logs")
        self.tabs.addTab(self.control_panel, "Control")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs)
        self.setCentralWidget(central)

        # Set up mock service
        self.mock_service = MockService(config_utils.load_config, self.update_status)
        self.control_panel.start_btn.clicked.connect(self.mock_service.start)
        self.control_panel.stop_btn.clicked.connect(self.mock_service.stop)
        self.control_panel.restart_btn.clicked.connect(self._restart_service)
        self.config_panel.save_btn.clicked.connect(self._reload_service_config)

    def update_status(self, status):
        # Update status panel with mock service data
        self.status_panel.job_count.setText(str(status.get("job_count", 0)))
        self.status_panel.last_dispatched.setText(status.get("last_dispatched", ""))
        self.status_panel.last_error.setText(status.get("last_error", ""))

    def _restart_service(self):
        self.mock_service.stop()
        self.mock_service.start()

    def _reload_service_config(self):
        # When config is saved, reload config in mock service
        self.mock_service.stop()
        self.mock_service = MockService(config_utils.load_config, self.update_status)
