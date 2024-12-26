import boto3
from datetime import datetime, timedelta
import time

def fetch_bt_sid_dynamic_window():
    """
    Fetch BT-SID metric (AVALABLE) with a dynamic window.
    """    
    try:        # Initialize CloudWatch client for Ireland region
        cloudwatch = boto3.client('cloudwatch', region_name='eu-west-1')

        # Metric parameters
        namespace = "*"
        metric_name = "*"
        statistic = "Average"
        period = 300
        max_window = 60
        window = 5
        backoff_factor = 2

        while window <= max_window:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=window)

            response = cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=[],
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=[statistic]
            )

            if response.get("Datapoints"):
                avg_value = sum(dp[statistic] for dp in response["Datapoints"]) / len(response["Datapoints"])
                return f"{avg_value:.2f}"
            window *= backoff_factor
            time.sleep(1)

        return "No data"
    except:
        return "Error"

def fetch_bt_sms_spent():
    """
    Fetch BT SMS Spent metric (SMSMonthToDateSpentUSD) from Ireland.
    """
    try:
        cloudwatch = boto3.client('cloudwatch', region_name='eu-west-1')

        response = cloudwatch.get_metric_statistics(
            Namespace="SNS",
            MetricName="USD",
            Dimensions=[],
            StartTime=datetime.utcnow() - timedelta(minutes=5),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=["Average"]
        )

        if response.get("Datapoints"):
            avg_value = response["Datapoints"][-1]["Average"]
            return f"{avg_value:.2f}"
        return "No data"
    except:
        return "Error"

bt_sms = fetch_bt_sms_spent()
bt_sid = fetch_bt_sid_dynamic_window()

if __name__ == "__main__":
    bt_sid = fetch_bt_sid_dynamic_window()
    bt_sms = fetch_bt_sms_spent()
    print(f"Value = {bt_sms}")
    print(f"Value = {bt_sid}")