# windows_printer.py
# All Windows-specific printer spooler logic using pywin32 must go here


import win32print
import win32api
import win32con

class WindowsPrinterAdapter:
    def __init__(self, printer_name):
        self.printer_name = printer_name

    def get_job_count(self):
        try:
            hPrinter = win32print.OpenPrinter(self.printer_name)
            jobs = win32print.EnumJobs(hPrinter, 0, 999, 1)
            win32print.ClosePrinter(hPrinter)
            return len(jobs)
        except Exception as e:
            return -1

    def is_printer_idle(self, threshold):
        job_count = self.get_job_count()
        return job_count >= 0 and job_count < threshold

    def get_status(self):
        try:
            hPrinter = win32print.OpenPrinter(self.printer_name)
            info = win32print.GetPrinter(hPrinter, 2)
            status = info['Status']
            win32print.ClosePrinter(hPrinter)
            if status == 0:
                return "Idle"
            elif status & win32con.PRINTER_STATUS_PRINTING:
                return "Busy"
            else:
                return "Unknown"
        except Exception:
            return "Unknown"
