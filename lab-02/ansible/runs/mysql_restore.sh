#!/bin/bash

set -e  # Exit on error

cd /data/src/mysql-backup || {
  echo "Directory /data/src/mysql-backup not found!"
  exit 1
}

if [[ ! -f "/data/backup/mysql/$1" ]]; then
  echo "Backup file '$1' not found in $(pwd)"
  exit 1
fi

.venv/bin/python3 restore.py "$1"
