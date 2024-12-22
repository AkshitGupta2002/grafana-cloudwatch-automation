import boto3
from datetime import datetime, timedelta

def fetch_upload_memory_utilization():
    """
    Fetch 'mem_used_percent' for the AutoScalingGroupName: H3O-UPLOAD-ASG.
    Displays the result as 'Memory Utilization = {} %'.
    """
    try:
        # Initialize CloudWatch client
        cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

        # Define query parameters
        namespace = "Production/Disk_Memory"
        metric_name = "mem_used_percent"
        dimensions = [{"Name": "AutoScalingGroupName", "Value": "H3O-UPLOAD-ASG"}]
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

        # Process results
        if "Datapoints" in response and response["Datapoints"]:
            sorted_datapoints = sorted(response["Datapoints"], key=lambda x: x["Timestamp"], reverse=True)
            latest_value = sorted_datapoints[0]["Average"]
            message = f"Memory Utilization = {latest_value:.2f}%" 
            return message
        
        message = "Memory Utilization = No data available." 
        return message

    except Exception as e:
        message = f"Memory Utilization = Error: {str(e)}" 
        return message

if __name__ == "__main__":
    print(fetch_upload_memory_utilization())






