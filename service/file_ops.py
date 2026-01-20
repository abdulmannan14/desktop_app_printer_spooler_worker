# file_ops.py
# Atomic file move and claim logic


import sys
if sys.platform == 'win32':
	from file_ops_win32 import atomic_rename, atomic_claim_file
else:
	def atomic_rename(src, dst):
		raise NotImplementedError("Atomic rename only supported on Windows.")
	def atomic_claim_file(src, dst, printer_id):
		raise NotImplementedError("Atomic claim only supported on Windows.")

