# Control Panel UI (stub)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Service (Mock)")
        self.stop_btn = QPushButton("Stop Service (Mock)")
        self.restart_btn = QPushButton("Restart Service (Mock)")
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.restart_btn)
        layout.addLayout(btn_layout)

        self.status_label = QLabel("Service status: Stopped (Mock)")
        layout.addWidget(self.status_label)

        self.start_btn.clicked.connect(self._start_service)
        self.stop_btn.clicked.connect(self._stop_service)
        self.restart_btn.clicked.connect(self._restart_service)

        layout.addStretch()

    def _start_service(self):
        self.status_label.setText("Service status: Running (Mock)")

    def _stop_service(self):
        self.status_label.setText("Service status: Stopped (Mock)")

    def _restart_service(self):
        self.status_label.setText("Service status: Restarting (Mock)")
