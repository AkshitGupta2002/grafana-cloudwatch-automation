import boto3
from datetime import datetime, timedelta
import time

def fetch_staging_sid_dynamic():
    """
    Fetch 'AVALABLE' metric from the staging account in North Virginia (us-east-1).
    Uses a dynamic time window to expand the query range if no data is found.
    """
    try:
        # Initialize CloudWatch client for North Virginia using staging profile
        session = boto3.Session(profile_name="staging", region_name="region")
        cloudwatch = session.client("cloudwatch")

        # Metric details
        namespace = "****"
        metric_name = "*****"
        period = 300  # 5-minute intervals
        max_window = 60  # Maximum window size in minutes
        window = 5  # Start with a 5-minute window
        backoff_factor = 2  # Exponential backoff

        # Dynamic window logic
        while window <= max_window:
            start_time = datetime.utcnow() - timedelta(minutes=window)
            end_time = datetime.utcnow()

            # Fetch the metric
            response = cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=[],  # No specific dimensions
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=["Average"]
            )

            # Process the response if data is found
            if response.get("Datapoints"):
                avg_value = sum(dp["Average"] for dp in response["Datapoints"]) / len(response["Datapoints"])
                return round(avg_value, 2)  # Return rounded value

            # Expand the time window if no data is found
            window *= backoff_factor
            time.sleep(1)  # Avoid throttling

        # If no data is found after the maximum window size
        return None

    except Exception as e:
        return None  # Return None in case of errors

staging_sid = fetch_staging_sid_dynamic()
if __name__ == "__main__":
    # Fetch the Staging SID value
    sid_value = fetch_staging_sid_dynamic()

    # Print the final output
    if sid_value is not None:
        print(f"SID = {sid_value}")
    else:
        print("SID = No data")