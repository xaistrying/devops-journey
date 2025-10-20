import os
from configs import *
from datetime import datetime
import subprocess
from modules import *
import gzip
from cryptography.fernet import Fernet

def backup():
    # Ensure backup dir exists
    if not os.path.exists(backup_dirpath):
        os.makedirs(backup_dirpath, exist_ok=True)

    # Ensure log file exists
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            pass

    # Backup
    timestamp = datetime.now().strftime(date_tag_format)
    filename = f"{DB_NAME}_backup_{timestamp}"
    filepath = os.path.join(backup_dirpath, filename + ".sql",)

    log("=" * 60)
    log("Starting MySQL back up...")

    try:
        log("Creating SQL dump...")
        with open(filepath, 'w') as f:
            subprocess.run(dump_cmd, stdout=f, check=True)

    except subprocess.CalledProcessError as e:
        log(f"Error during backup process: {e.stderr.decode()}", Logging.ERROR)
        log("Backup process stopped due to error.", Logging.ERROR)
        if os.path.exists(filepath):
            os.remove(filepath)
        return

    except Exception as e:
        log(f"Unexpected error during backup: {e}", Logging.ERROR)
        if os.path.exists(filepath):
            os.remove(filepath)
        return

    # Compress
    compressed_filepath = os.path.join(backup_dirpath, filename + ".gz")

    log("Compressing backup file...")
    try:
        with open(filepath, 'rb') as f_in:
            with gzip.open(compressed_filepath, 'wb') as f_out:
                f_out.writelines(f_in)

        os.remove(filepath)

    except Exception as e:
        log(f"Compression failed: {e}", Logging.ERROR)
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(compressed_filepath):
            os.remove(compressed_filepath)
        return

    # Encrypt
    if not ENCRYPTION_KEY:
        log("Encryption key not configured", Logging.ERROR)
        if os.path.exists(compressed_filepath):
            os.remove(compressed_filepath)
        return

    log("Encrypting backup file...")

    encrypted_filepath = os.path.join(backup_dirpath, filename + ".enc")
    try:
        cipher = Fernet(ENCRYPTION_KEY.encode())

        with open(compressed_filepath, 'rb') as f:
            data = f.read()

        encrypted_data = cipher.encrypt(data)

        with open(encrypted_filepath, 'wb') as f:
            f.write(encrypted_data)

        os.remove(compressed_filepath)

    except Exception as e:
        log(f"Encryption failed: {e}", Logging.ERROR)
        if os.path.exists(encrypted_filepath):
            os.remove(encrypted_filepath)
        return

    # Complete
    log("Backup and encryption completed successfully.")

if __name__ == "__main__":
    backup()
