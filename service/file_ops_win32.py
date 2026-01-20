# file_ops_win32.py
# Windows-only atomic file operations for job claiming

import os
import shutil
import time
import msvcrt

def atomic_rename(src, dst):
    """
    Atomically rename src to dst (same volume).
    """
    os.replace(src, dst)


def atomic_claim_file(src, dst, printer_id):
    """
    Claim a file for processing. Handles same and cross-volume moves.
    Returns True if claimed, False otherwise.
    """
    try:
        # Try atomic rename (same volume)
        atomic_rename(src, dst)
        return True
    except OSError:
        # Cross-volume: lock, copy, flush, verify, delete
        try:
            with open(src, 'rb') as fsrc:
                msvcrt.locking(fsrc.fileno(), msvcrt.LK_NBLCK, 1)
                with open(dst, 'wb') as fdst:
                    shutil.copyfileobj(fsrc, fdst)
                    fdst.flush()
                    os.fsync(fdst.fileno())
                msvcrt.locking(fsrc.fileno(), msvcrt.LK_UNLCK, 1)
            # Verify size
            if os.path.getsize(src) == os.path.getsize(dst):
                os.remove(src)
                return True
            else:
                os.remove(dst)
                return False
        except Exception:
            return False
