# Utility for config read/write
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

DEFAULT_CONFIG = {
    "printer_name": "",
    "master_folder_path": "",
    "printer_hot_folder_path": "",
    "allowed_file_extensions": "pdf,txt",
    "spooler_job_threshold": 1,
    "polling_interval": 10,
    "minimum_file_age": 30,
    "log_file_path": "printer_service.log"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
