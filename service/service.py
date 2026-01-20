# service.py
# Windows Service entry point using pywin32


import win32serviceutil
from winservice_utils import PrinterSpoolerService

if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(PrinterSpoolerService)

