import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv("./.env")

# Database configs
DB_NAME = os.getenv("DB_NAME", "mysql")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST", "localhost")

# Backup configs
BACKUP_DIR = os.getenv("BACKUP_DIR", "/data/backup/mysql")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "7"))

# Paths
backup_dir_path = os.path.expanduser(BACKUP_DIR)
log_path = os.path.expanduser(f"{BACKUP_DIR}/backup.log")

# Time format
time_format_str = "%d/%m/%Y-%H:%M:%S"
date_tag_format = "%d%m%Y"

# Notification configs
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Encryption configs
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# MySQL dump command
dump_cmd = [
    "mysqldump",
    f"-u{DB_USER}",
    "--all-databases",
    "--quick",
]

# Enum
class Logging(Enum):
    INFO = "INFO"
    ERROR = "ERROR"

    def __str__(self):
        return self.value
