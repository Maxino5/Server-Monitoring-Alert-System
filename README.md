# Server Monitoring and Alert System

A Python utility designed to monitor the availability of websites and servers. It performs periodic health checks, logs status updates to a local file, and sends instant email notifications if a target site becomes unreachable.

## 🚀 Features
* **Real-time Monitoring:** Periodic checks of multiple URLs.
* **Instant Alerts:** Email notifications for both downtime and recovery.
* **Detailed Logging:** Keeps a history of all events in `system_log.txt`.
* **Terminal Dashboard:** Clean visual output of current server status and response times.

## 🛠️ Prerequisites
* Python 3.x
* `requests` library

```bash
pip install requests
