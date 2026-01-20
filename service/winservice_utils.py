# winservice_utils.py
# Utilities for Windows Service registration and control

import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import sys
import logging

class PrinterSpoolerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PrinterSpoolerWorker"
    _svc_display_name_ = "Printer Spooler Worker Service"
    _svc_description_ = "Monitors printer queue and dispatches jobs from master folder."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, "Service started"))
        self.main()

    def main(self):
        # Import dispatcher and run main loop
        import dispatcher
        dispatcher.run_service_loop()
        # Wait for stop event
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
