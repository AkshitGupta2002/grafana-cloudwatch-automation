import boto3
from datetime import datetime, timedelta

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Function to fetch the ORBWEB -> AVALABLE metric (Sum statistic)
def fetch_hubble_sid_message():
    try:
        # Define the CloudWatch metric parameters
        hubble_sid_metric = {
            "Namespace": "*",
            "MetricName": "*",  # Metric name
            "Dimensions": [],
            "Statistics": ["Sum"],  # Sum statistic
        }

        # Set a fixed 2-minute window
        end_time = datetime.utcnow().replace(second=0, microsecond=0)
        start_time = end_time - timedelta(minutes=2)

        # Fetch metric data from CloudWatch
        response = cloudwatch.get_metric_statistics(
            Namespace=hubble_sid_metric["Namespace"],
            MetricName=hubble_sid_metric["MetricName"],
            Dimensions=hubble_sid_metric["Dimensions"],
            StartTime=start_time,
            EndTime=end_time,
            Period=120,  # 2 minutes in seconds
            Statistics=hubble_sid_metric["Statistics"]
        )

        # Process the response if data is available
        if response and response["Datapoints"]:
            total_sum = sum(dp["Sum"] for dp in response["Datapoints"])  # Sum of all datapoints
            message = f"ID = {total_sum:.0f}"
            return message # Format the sum as an integer

        message = "ID = No data available"
        return message

    except Exception as e:
        message = f"ID = Error: {str(e)}"
        return message
