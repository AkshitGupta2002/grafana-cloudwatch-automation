import boto3
from datetime import datetime, timedelta
import time

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Function to convert bytes based on the condition
def format_size(bytes_size):
    if bytes_size > 1_000_000_000_000:  # Greater than 1 TB
        return f"{bytes_size / 1_000_000_000_000:.2f} TB"
    else:  # Convert to GB
        return f"{bytes_size / 1_000_000_000:.2f} GB"

# Function to fetch EFS size and return the formatted message
def fetch_efs_metric_message():
    try:
        # Define EFS metric parameters
        efs_metric = {
            "Namespace": "AWS/EFS",
            "MetricName": "StorageBytes",
            "Dimensions": [
                {"Name": "FileSystemId", "Value": "**"}
            ],
            "Statistics": ["Sum"]
        }

        # Start with a 5-minute time window
        initial_window_minutes = 5
        max_window_minutes = 60  # Maximum window size of 60 minutes
        backoff_factor = 2  # Exponential backoff factor
        current_window = initial_window_minutes

        while current_window <= max_window_minutes:
            # Define the time window for the current iteration
            end_time = datetime.utcnow().replace(second=0, microsecond=0)
            start_time = end_time - timedelta(minutes=current_window)

            # Fetch the metric
            response = cloudwatch.get_metric_statistics(
                Namespace=efs_metric["Namespace"],
                MetricName=efs_metric["MetricName"],
                Dimensions=efs_metric["Dimensions"],
                StartTime=start_time,
                EndTime=end_time,
                Period=current_window * 60,  # Period in seconds
                Statistics=efs_metric["Statistics"]
            )

            # Check if data is available
            if response and response["Datapoints"]:
                # Process the data
                total_sum = sum(dp["Sum"] for dp in response["Datapoints"])
                formatted_size = format_size(total_sum)
                message = f"EFS = {formatted_size}"
                return message

            # Expand the time window exponentially and retry
            current_window *= backoff_factor
            time.sleep(1)  # Optional: Add a small delay before retrying

        message = "EFS = No data available"
        return message

    except Exception as e:
        message = f"EFS = Error: {str(e)}"
        return message

