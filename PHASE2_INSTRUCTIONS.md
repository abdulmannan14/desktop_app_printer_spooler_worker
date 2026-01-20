# Project Phase 2 – Core Functionality (Windows)

## Context
- Phase 1 (UI + config editor + mock logic) is complete and must not be redesigned.
- We are now working on Windows.
- The app is written in Python.
- Each instance of the app manages exactly one printer.
- The UI already reads/writes config.json; Phase 2 must consume the same config without changes.

## Phase 1 Status (DO NOT MODIFY)
- UI screens (Config, Status, Logs, Controls)
- config.json schema
- UI → config read/write
- Mock service loop used for UI testing

⚠️ Do not refactor UI or config structure unless explicitly instructed.

## Phase 2 Goal
Replace all mocks with real Windows behavior, implement the dispatcher logic, and package the app as a Windows Service + standalone UI controller.

## Phase 2 Functional Requirements
1. **Windows Service Implementation**
   - Implement a real Windows Service using pywin32.
   - Service must start automatically with Windows, run without UI, read config.json on startup, and write logs continuously.
   - UI must act only as config editor, status viewer, and service controller (start/stop/restart).
2. **Printer Queue Monitoring**
   - Use Win32 Print Spooler APIs via pywin32: OpenPrinter, EnumJobs.
   - Determine printer availability by job count < config.spooler_job_threshold.
   - Poll at config.poll_interval_seconds.
3. **Master Folder Scanning**
   - Master folder is a shared network path.
   - Scan only files that match allowed extensions and have file age ≥ config.min_file_age_seconds.
   - Sort by oldest first.
4. **Atomic Job Claiming (Critical)**
   - Only ONE service instance may claim a file.
   - Same Volume: Use os.replace() to atomically rename job.pdf → job.claimed.<printer_id>.
   - Cross Volume: Lock source file, copy to destination, flush & verify file size, delete source.
   - If claiming fails → move to next candidate.
5. **Dispatch to Printer Hot Folder**
   - Move claimed file into printer’s hot folder using final atomic rename.
   - Once placed, do not track job outcome (external automation handles success/error).
6. **Logging**
   - Log file path comes from config.
   - Log service start/stop, printer queue status, job claimed, job dispatched, errors & retries.
   - Use timestamped, append-only logs (TXT or CSV).
7. **Error Handling Rules**
   - Service must never crash due to network glitches, file locks, printer unavailability.
   - Retry transient failures. Log permanent failures clearly.

## Architecture Rules (MANDATORY)
- Strict separation of concerns:
  - `/ui/`                  # existing UI code (unchanged)
  - `/service/`
    - dispatcher.py    # job selection & claiming
    - printer_probe.py # spooler queries
    - file_ops.py      # atomic moves
    - service.py       # Windows service entry
  - `/config/`
    - config.json
- All Windows-only code must live in printer_probe.py and service.py.
- Core logic must be testable without the UI.
