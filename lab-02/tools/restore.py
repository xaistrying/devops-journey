import sys
from modules import *
from cryptography.fernet import Fernet
import gzip
import subprocess

def list_backups():
    backups = []
    for filename in sorted(os.listdir(backup_dirpath)):
        # find all file as "mysql_backup_*.enc"
        if filename.startswith(f"{DB_NAME}_backup_") and filename.endswith(".enc"):
            filepath = os.path.join(backup_dirpath, filename)

            # retrieve the last modification time
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'filepath': filepath,
                'date': file_time.strftime(time_format_str),
            })
    return backups

def decrypt_file(input_file: str, output_file: str):
    if not ENCRYPTION_KEY:
        raise Exception("Encryption key not configured")

    log("Decrypting backup file...")
    try:
        cipher = Fernet(ENCRYPTION_KEY.encode())

        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        log(f"Decryption completed: {output_file}")
    except Exception as e:
        raise Exception(f"Decryption failed: {e}")

def decompress_file(input_file: str, output_file: str):
    log("Decompressing backup file...")
    try:
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.writelines(f_in)
        log(f"Decompression completed: {output_file}")
    except Exception as e:
        raise Exception(f"Decompression failed: {e}")

def restore_database(sql_file: str):
    log("Restoring database...")
    try:
        restore_cmd = [
            "mysql",
            f"-h{DB_HOST}",
            f"-u{DB_USER}",
        ]

        with open(sql_file, 'r') as f:
            result = subprocess.run(
                restore_cmd,
                stdin=f,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )

        log("Database restored successfully!")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Database restore failed: {e.stderr}")

def restore(backup_filename: str = None):
    log("=" * 60)
    log("Starting MySQL restore process...")

    try:
        backups = list_backups()

        if not backups:
            log("No backup files found!", Logging.ERROR)
            return

        if backup_filename:
            selected_backup: str = None
            for backup in backups:
                if backup['filename'] == backup_filename:
                    selected_backup = backup
                    break
            if not selected_backup:
                log(f"Backup file not found: {backup_filename}", Logging.ERROR)
                return

        log(f"Selected backup: {selected_backup['filename']}")

        # Prepare
        temp_dir = os.path.join(backup_dirpath, "temp_restore")
        os.makedirs(temp_dir, exist_ok=True)

        base_name = selected_backup['filename'].replace(".enc", "")
        gz_file = os.path.join(temp_dir, f"{base_name}.gz")
        sql_file = os.path.join(temp_dir, f"{base_name}.sql")

        # Decrypt
        log("Decrypting backup file...")
        decrypt_file(selected_backup['filepath'], gz_file)

        # Decompress
        log("Decompressing backup file...")
        decompress_file(gz_file, sql_file)

        # Restore
        log("Restoring database...")
        restore_database(sql_file)

        # Cleanup temp files
        os.remove(gz_file)
        os.remove(sql_file)
        os.rmdir(temp_dir)

    except Exception as e:
        log(f"Error during restore process: {str(e)}", Logging.ERROR)
        log("Restore process stopped due to error.", Logging.ERROR)
        return

if __name__ == "__main__":
    backup_file = sys.argv[1] if len(sys.argv) > 1 else None
    exit(restore(backup_file))
