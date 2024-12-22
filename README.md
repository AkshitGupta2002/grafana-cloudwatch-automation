# Hourly Updates Automation ⏰

This project automates the process of hourly updates reported by the L1 team for various server metrics. The automation uses AWS CloudWatch to scrape metrics and a Python script to send the data to a Skype group via the `skpy` library. The entire process ensures accurate and timely reporting while reducing manual intervention. 

---

## 🔧 Architecture Overview
In Hubble, metrics are displayed on a Grafana dashboard using various data sources like AWS CloudWatch and Prometheus. For hourly updates, the key data source is **CloudWatch**, which covers both **Production** and **Staging** environments. Below is a summary of the architecture:

- **Data Sources:**
  - AWS CloudWatch (Primary for hourly reporting)
  - Prometheus (Selective metrics, not included in hourly updates)
- **Regions:**
  - Production: **North Virginia** and **Ireland (BT Stack)**
  - Staging: **North Virginia (Staging SID)**

Metrics are fetched using **Boto3**, the official AWS SDK for Python, which interacts with CloudWatch to retrieve the required data.

---

## 👨‍💻 File Structure
The directory structure of the project is as follows:

```
file_folder/skype_automation
|
├── collect_metrics.py      # Core script to scrape and organize metrics
├── update.py               # Sends the data to the Skype group
├── Hubble_SID.py           # Handles staging SID-specific metrics
├── bt_stack.py             # Handles BT Stack (Ireland region) metrics
├── staging_SID.py          # Handles staging metrics for North Virginia
├── UDP.py                  # Scrapes UDP metrics
├── upload_mem_util.py      # Handles memory utilization metrics
```

- **`collect_metrics.py`**: Main script to collect all metrics.
- **`update.py`**: Sends the collected metrics to Skype using the `skpy` library.
- **Separate Files**: Certain metrics (e.g., UDP, SIDs) are handled differently due to their specific requirements.

---

## 🔧 Setup and Requirements

### Prerequisites
Ensure the following are installed and configured:
- **Python 3.x**
- **AWS credentials** configured for both **Staging** and **Production** accounts (stored securely in the Hubble-TD-Agent-1 server).
- **Python Libraries:**
  - `boto3`
  - `skpy`

Install dependencies using:
```bash
pip install boto3 skpy
```

---

## ⚡ Dynamic Window and Exponential Backoff
This project uses two key techniques to handle discrepancies in metric availability:

- **Exponential Backoff**: Retries API calls with increasing delay if no data is returned. After 3 retries, displays `0` as a fallback.
- **Dynamic Window Approximation**: Expands the time window for querying metrics if no data is found within the initial range (up to 5 minutes).

These methods ensure reliability and accuracy even when metric data is inconsistent.

---

## ⏳ Setting up Cron
The `update.py` script is scheduled to run via a cron job:
- **Schedule:** `hh:57` (3 minutes before the hour)
- This timing ensures that metrics scraped at 5-minute intervals are accurately processed without missing data.

Example crontab entry:
```bash
57 * * * * python3 /path/to/update.py
```

---

## 🔬 Example Output
### Command Line Output
```plaintext
Number of healthy hosts: 5
API Latency: 120ms
CS Latency: 150ms
Upload Latency: 180ms
```
### Skype Output
```
Hourly Metrics Update:
- Healthy Hosts: 5
- API Latency: 120ms
- CS Latency: 150ms
- Upload Latency: 180ms
```

---

## ⚠ How to Run the Code
To execute the automation, use the following command:
```bash
python3 main.py
```
This will:
1. Scrape metrics from CloudWatch using `collect_metrics.py`
2. Send the hourly update to the configured Skype group via `update.py`.

---

## 🎉 Contributions and Feedback
Contributions are welcome! Feel free to open issues or submit pull requests. If you encounter any problems, please let us know. 

Happy Automating! 🚀

