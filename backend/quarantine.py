import os
import shutil

QUARANTINE_DIR = "quarantine"

def quarantine_file(file_path, file_hash):
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    if not os.path.exists(file_path):
        return None
        
    new_name = f"{file_hash}.blocked"
    q_path = os.path.join(QUARANTINE_DIR, new_name)
    
    try:
        shutil.move(file_path, q_path)
        return q_path
    except Exception:
        # If it fails (maybe already exists), just return the path where it should be
        if os.path.exists(q_path):
            return q_path
        return None
