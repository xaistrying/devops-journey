import sys
from modules import *

def list_backups():
    backups = []
    for filename in sorted(os.listdir(backup_dirpath)):
        # find all file as "mysql_backup_*.enc"
        if filename.startswith(f"{DB_NAME}_backup_") and filename.endswith(".enc"):
            filepath = os.path.join(backup_dirpath, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_size = os.path.getsize(filepath)
            backups.append({
                'filename': filename,
                'filepath': filepath,
                'date': file_time.strftime(time_format_str),
                'size': file_size
            })
    return backups

def restore(backup_filename: str = None):
    log("=" * 60)
    log("Starting MySQL restore process...")

    backup_filepath = os.path.join(backup_dirpath, backup_filename)

    backups = list_backups()

    if not backups:
        log("No backup files found!", Logging.ERROR)
        return

    if backup_filename:
        selected_backup: str = None
        for backup in backups:
            if backup['filename'] == backup_filename:
                selected_backup = backup['filename']
                break
        if not selected_backup:
            log(f"Backup file not found: {backup_filename}", Logging.ERROR)
            return

if __name__ == "__main__":
    backup_file = sys.argv[1] if len(sys.argv) > 1 else None
    exit(restore(backup_file))
