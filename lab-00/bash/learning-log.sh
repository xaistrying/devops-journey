#!/bin/bash

# var

user_name=$(whoami)
hour=$(date +%-H)
formatted_date=$(date +"%d-%m-%Y")

learning_time=$1
subjects=("${@:2}")

log_file="$HOME/learning-log.md"

hour_text="hours"
if [[ "${learning_time}" =~ ^[0-9]+$ ]] && [ "${learning_time}" -eq 1 ]; then
    hour_text="hour"
fi

# greeting

function greeting() {
    if [ "$hour" -ge 6 ] && [ "$hour" -lt 12 ]; then
        echo "Good morning, ${user_name}! Hope you will have a nice day."
    elif [ "$hour" -ge 12 ] && [ "$hour" -lt 18 ]; then
        echo "Good afternoon, ${user_name}! Hope you will have a nice day."
    else
        echo "Good evening, ${user_name}! Hope you had a nice day."
    fi
}

printf "\n$(greeting)\n\n"

# write log to learning-log.md

function log_content() {
    printf "# Date: ${formatted_date}\n"
    printf "%s\n" "- Time spent: ${learning_time} ${hour_text}"
    printf "%s\n" "- Learning covered:"
    for subject in "${subjects[@]}"; do
        printf "    + %s\n" "${subject}"
    done
}

log_content
printf "\n"

printf "Would you like to write this into ~/learning-log.md file? (Y/n): "
read option

if [ "$option" == "y" ] || [ "$option" == "Y" ]; then

    # create the file if it does not exist

    if [ ! -f "$log_file" ]; then
        touch "$log_file"
    fi

    # check if log file already contains an entry with today's date

    if grep -q "^# Date: ${formatted_date}" "${log_file}"; then
        printf "Entry for today already exists. Would you like to overwrite it? (Y/n): "
        read option2

        if [ "$option2" != "y" ] && [ "$option2" != "Y" ]; then
            printf "Log not saved. Exiting."
            exit 0
        fi

        # delete today's log entry from the file
        sed -i "/^# Date: ${formatted_date}/,/^$/d" "$log_file"
    fi

    # write log

    log_content >> "${log_file}"
    printf "Log entry saved to ~/learning-log.md"
else
    printf "%s\n" "Log not saved. Exiting."
fi
