
# windows_service.py
# All Windows Service logic using pywin32 must go here

import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import json
import traceback
from dispatcher import Dispatcher
from windows_printer import WindowsPrinterAdapter

class WindowsPrinterService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PrinterAutomationService"
    _svc_display_name_ = "Printer Automation Service"
    _svc_description_ = "Manages printer job dispatch from network folder."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Printer Automation Service started.")
        self.main()


    def main(self):
        # Main service loop with dispatcher logic
        def log_callback(msg):
            try:
                with open(self.config.get('log_file_path', 'printer_service.log'), 'a') as f:
                    f.write(f"{msg}\n")
            except Exception:
                servicemanager.LogErrorMsg(f"Failed to write log: {msg}")

        printer = WindowsPrinterAdapter(self.config.get('printer_name', ''))
        dispatcher = Dispatcher(self.config, printer, log_callback)
        dispatcher.start()
        try:
            while self.running:
                win32event.WaitForSingleObject(self.hWaitStop, 1000)
        except Exception as e:
            servicemanager.LogErrorMsg(f"Service error: {e}\n{traceback.format_exc()}")
        finally:
            dispatcher.stop()

# Entry point for service registration
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WindowsPrinterService)
