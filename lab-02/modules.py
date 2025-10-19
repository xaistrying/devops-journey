from datetime import datetime
from configs import *
import requests

def log(message: str, level: Logging = Logging.INFO):
    time = datetime.now().strftime(time_format_str)
    log_message = f"[{time}] [{str(level).ljust(5)}] {message}\n"

    with open(log_path, "a") as f:
        f.write(log_message)

def send_discord_notification(title: str, description: str, value: str):
    if not DISCORD_WEBHOOK_URL:
        log("DISCORD_WEBHOOK_URL not configured in .env", "ERROR")
        return

    embed = {
        "title": title,
        "description": description,
        "color": 0x3498db,
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {"name": "Status", "value": value, "inline": True},
            {"name": "Time", "value": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "inline": True}
        ],
        "footer": {
            "text": "MySQL Backup System"
        }
    }

    payload = {"embeds": [embed]}

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code in [200, 204]:
            log("Discord notification sent successfully!")
        else:
            log(
                f"Failed to send Discord notification: {response.status_code} - {response.text}",
                Logging.ERROR)
    except Exception as e:
        log(f"Failed to send Discord notification: {e}", Logging.ERROR)
