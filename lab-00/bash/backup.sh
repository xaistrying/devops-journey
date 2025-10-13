#!/bin/bash

# --- Variables ---
default_backup_dir="$HOME/backups"

# --- Functions ---
show_help() {
    printf "%s\n" "USAGE:"
    printf "  %s\n" "bash backup.sh [OPTIONS]"

    printf "\n%s\n" "OPTIONS:"
    printf "  %-25s %s\n" "-c, --create  SOURCE_DIR [BACKUP_DIR]"
    printf "  %-25s %s\n" "" "Create a backup of SOURCE_DIR into BACKUP_DIR" 
    printf "  %-25s %s\n" "" "If BACKUP_DIR is not provided, it defaults to ~/backups" 
    printf "\n"
    printf "  %-25s %s\n" "-l, --list" "List all backup files in BACKUP_DIR"
    printf "  %-25s %s\n" "-h, --help" "Display this help and exit"
    printf "\n"
    printf "  %-25s %s\n" "-r, --restore [latest|FILE] [BACKUP_DIR] [RESTORE_DIR]" 
    printf "  %-25s %s\n" "" "Restore from the latest or a specified backup"
}

check_backup_dir() {
    backup_dir=$1

    if [ -z "${backup_dir}" ]; then
        backup_dir="${default_backup_dir}"
    fi

    if [ ! -d "${backup_dir}" ]; then
        mkdir "${backup_dir}"
    fi
}

get_source_name() {
    printf "$(basename "$1")"
}

list_backups() {
    check_backup_dir "$1"

    ls -lht "${backup_dir}"/*.tar.gz 2>/dev/null || printf "No backups found"
}

create_backup() {
    source_dir="$1"
    backup_dir="$2"
    source_name=$(get_source_name "${source_dir}")

    if [ ! -d "${source_dir}" ]; then 
        printf "Error: Source directory does not exist!"
        exit 1
    fi

    if [ -z "${backup_dir}" ]; then
        backup_dir="${default_backup_dir}"
    fi

    check_backup_dir "${backup_dir}"

    timestamp=$(date +"%Y%m%dT%H%M%S%Z")
    source_name=$(basename "${source_dir}")
    backup_file="${source_name}-${timestamp}.tar.gz"

    # tar -> programs that makes archive file
    # -c -> create new archive
    # -z -> compress with gzip (tar.gz)
    # -f file -> output filename
    # -C "$(dirname "$source_dir")" -> switch into the parent directory of $source_dir before creating the archive.
    # "$(basename "${source_dir}")" -> archive just the folder name
    tar -czf "${backup_dir}/${backup_file}" -C "$(dirname "${source_dir}")" "$(basename "${source_dir}")"

    # -P -> keep absolute path
    # tar -czPf "${backup_dir}/${backup_file}" "${source_dir}"

    # $? -> holds the exit status of the last executed command 
    if [ $? -eq 0 ]; then
        printf "%s\n" "Backup saved to: ${backup_dir}/${backup_file}"
    else
        printf "%s\n" "Backup failed!"
    fi
}

restore_backup() {
    backup_dir="$2"
    backup_file=""
    
    if [ -z "${backup_dir}" ]; then
        backup_dir="${default_backup_dir}"
    fi

    case "$1" in
        "latest")
            # ls -t -> sort by time, newest first
            backup_file=$(ls -t "${backup_dir}"/*.tar.gz 2>/dev/null | head -n 1)
            ;;
        *)
            filename="$1"
            [[ "$filename" != *.tar.gz ]] && filename="${filename}.tar.gz"
            backup_file="${backup_dir}/${filename}"
            ;;
    esac

    if [ ! -f "${backup_file}" ]; then
        printf "No backups found in ${backup_dir}\n"
        exit 1
    fi

    if [ -z "$3" ]; then
        tar -xzf "${backup_file}"
        printf "Restored latest backup into current directory.\n"
    else
        if [ ! -d "$3" ]; then
            mkdir -p "$3"
        fi
        tar -xzf "${backup_file}" -C "$3"
        printf "Restore latest backup into %s\n" "$3"
    fi
}

# --- Main ---
case "$1" in
    --help|-h)
        show_help
        ;;
    --list|-l)
        list_backups $2
        ;;
    --create|-c)
        create_backup $2 $3
        ;;
    --restore|-r)
        restore_backup $2 $3 $4
        ;;
    *)
        show_help
        exit 1
        ;;
esac