# Main window for Printer Automation UI

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from .config_panel import ConfigPanel
from .status_panel import StatusPanel
from .logs_panel import LogsPanel
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

        self.tabs.addTab(self.config_panel, "Configuration")
        self.tabs.addTab(self.status_panel, "Status / Monitoring")
        self.tabs.addTab(self.logs_panel, "Logs")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.tabs)
        self.setCentralWidget(central)




