import boto3
from datetime import datetime, timedelta

def fetch_udp_memory_utilization():
    """
    Fetch and display only the memory utilization value.
    """
    try:
        # Initialize CloudWatch client
        cloudwatch = boto3.client('cloudwatch')

        # Define metric query parameters
        namespace = "Production/Disk_Memory"
        metric_name = "mem_used_percent"
        dimensions = [
            {"Name": "InstanceId", "Value": "i-0282efd00ccd6aea6"},
            {"Name": "ImageId", "Value": "ami-02c7b3e78b137c2f5"},
            {"Name": "InstanceType", "Value": "m5.large"}
        ]
        period = 300  # 5-minute intervals
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=6)  # Query last 6 hours

        # Fetch metric statistics
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=["Average"]
        )

        # Process and display memory utilization
        if "Datapoints" in response and response["Datapoints"]:
            sorted_datapoints = sorted(response["Datapoints"], key=lambda x: x["Timestamp"], reverse=True)
            latest_value = sorted_datapoints[0]["Average"]
            message = f"{latest_value:.2f}%"
            return message
        else:
            message = "No data available." 
            return message

    except Exception as e:
        message = f"Error: {str(e)}"
        return message

