# Status / Monitoring Panel UI (stub)

from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer

class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._mock_status()

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

        # Refresh button for mock
        self.refresh_btn = QPushButton("Refresh (Mock)")
        self.refresh_btn.clicked.connect(self._mock_status)
        layout.addWidget(self.refresh_btn)

    def _mock_status(self):
        # Simulate status values
        import random, datetime
        self.service_status.setText(random.choice(["Running (Mock)", "Stopped (Mock)"]))
        self.printer_status.setText(random.choice(["Idle (Mock)", "Busy (Mock)", "Unknown (Mock)"]))
        self.job_count.setText(str(random.randint(0, 5)))
        self.last_dispatched.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.last_error.setText(random.choice(["", "No paper (Mock)", "Connection lost (Mock)"]))
