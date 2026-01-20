# printer_probe_win32.py
# Windows-only printer queue monitoring using pywin32

import win32print
import win32api
import pywintypes

def get_printer_job_count(printer_name):
    """
    Returns the number of jobs in the specified printer's queue.
    """
    try:
        handle = win32print.OpenPrinter(printer_name)
        jobs = win32print.EnumJobs(handle, 0, 999, 1)
        win32print.ClosePrinter(handle)
        return len(jobs)
    except pywintypes.error as e:
        return -1  # Indicates error


def is_printer_available(printer_name, job_threshold):
    """
    Returns True if the printer's job count is below the threshold.
    """
    job_count = get_printer_job_count(printer_name)
    if job_count == -1:
        return False
    return job_count < job_threshold
