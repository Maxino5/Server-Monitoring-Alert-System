import requests
import smtplib
import time
import logging
from email.message import EmailMessage

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    filename="system_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# Configuration
# -----------------------------
TARGET_SITES = [
    "https://www.google.com",
    "https://github.com",
    "https://thenkiri.com",
    "https://thiswebsitedoesnotexist123.com"
]

EMAIL_ADDRESS = "YOUR-EMAIL@gmail.com"
EMAIL_PASSWORD = "PASSWORD"
RECEIVER_EMAIL = "RECEIVER-EMAIL@gmail.com"

CHECK_INTERVAL = 60  # seconds between checks

# Track site state
site_status = {site: True for site in TARGET_SITES}

# -----------------------------
# Email Alert Function
# -----------------------------
def send_email(subject, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email notification sent.")
    except Exception as e:
        print(f"Email sending failed: {e}")

# -----------------------------
# Terminal Dashboard
# -----------------------------
def display_status(site, status, response_time=None, error=None):
    print("\n==============================")
    print("PYTHON SERVER MONITOR")
    print(f"Target: {site}")

    if status == "ONLINE":
        print("Status: ONLINE")
        print(f"Response Time: {response_time}s")
    else:
        print("Status: OFFLINE")
        print(f"Error: {error}")

    print(f"Last Check: {time.strftime('%H:%M:%S')}")
    print("==============================")

# -----------------------------
# Monitoring Function
# -----------------------------
def monitor_sites():
    print("\nStarting monitoring service...\n")

    while True:
        for site in TARGET_SITES:

            try:
                start_time = time.time()
                response = requests.get(site, timeout=10)
                response_time = round(time.time() - start_time, 3)

                if response.status_code == 200:

                    display_status(site, "ONLINE", response_time)
                    logging.info(f"{site} ONLINE - {response_time}s")

                    # Recovery detection
                    if site_status[site] == False:
                        send_email(
                            f"RECOVERY: {site} is back online",
                            f"The server at {site} has recovered.\nResponse time: {response_time}s"
                        )

                    site_status[site] = True

                else:
                    raise Exception(f"Status Code {response.status_code}")

            except Exception as e:

                display_status(site, "OFFLINE", error=e)
                logging.error(f"{site} OFFLINE - {e}")

                # Send alert only if it was previously online
                if site_status[site] == True:
                    send_email(
                        f"CRITICAL ALERT: {site} is DOWN",
                        f"The server at {site} is unreachable.\nError: {e}"
                    )

                site_status[site] = False

        time.sleep(CHECK_INTERVAL)

# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    monitor_sites()