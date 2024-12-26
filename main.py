import boto3
import time
from datetime import datetime, timedelta
from size import fetch_efs_metric_message  # Import EFS Size function
from ids import fetch_hubble_sid_message  # Import Hubble SID function
from datetime import datetime
from mem_util2 import fetch_udp_memory_utilization
from mem_util import fetch_SERVER3_memory_utilization
from region2 import bt_sms, bt_sid
from staging_SID import staging_sid

# Initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# Metric configurations for SERVER1, CS, and SERVER3
metrics_config = {
    "SERVER1": {
        "latency": {
            "Namespace": "ELB",
            "MetricName": "TargetResponseTime",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "healthy_hosts": {
            "Namespace": "ELB",
            "MetricName": "HealthyHostCount",
            "Dimensions": [
                {"Name": "LoadBalancer", "Value": "**"},
                {"Name": "TargetGroup", "Value": "**"}
            ],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "Request_Count": {
            "Namespace": "ELB",
            "MetricName": "RequestCount",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_2XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_2XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_3XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_3XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_4XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_4XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_5XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_5XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "ELB_4XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_ELB_4XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "ELB_5XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_ELB_5XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        }
    },
    "CS": {
        "latency": {
            "Namespace": "ELB",
            "MetricName": "TargetResponseTime",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "healthy_hosts": {
            "Namespace": "ELB",
            "MetricName": "HealthyHostCount",
            "Dimensions": [
                {"Name": "LoadBalancer", "Value": "**"},
                {"Name": "TargetGroup", "Value": "**"}
            ],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "Request_Count": {
            "Namespace": "ELB",
            "MetricName": "RequestCount",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_2XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_2XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_3XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_3XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_4XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_4XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_5XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_5XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "ELB_4XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_ELB_4XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "ELB_5XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_ELB_5XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        }
    },
    "SERVER3": {
        "latency": {
            "Namespace": "ELB",
            "MetricName": "TargetResponseTime",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "in_service_instances": {
            "Namespace": "AutoScaling",
            "MetricName": "GroupInServiceInstances",
            "Dimensions": [{"Name": "AutoScalingGroupName", "Value": "ASG"}],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "Request_Count": {
            "Namespace": "ELB",
            "MetricName": "RequestCount",
            "Dimensions": [
                {"Name": "LoadBalancer", "Value": "**"},
                {"Name": "TargetGroup", "Value": "**"}
            ],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_4XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_4XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        },
        "HTTP_5XX": {
            "Namespace": "ELB",
            "MetricName": "HTTPCode_Target_5XX_Count",
            "Dimensions": [{"Name": "LoadBalancer", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Sum"]
        }
    },
    "SmartAnalytics": {
        "healthy_hosts": {
            "Namespace": "AWS",
            "MetricName": "GroupTotalInstances",
            "Dimensions": [{"Name": "AutoScalingGroupName", "Value": "SMART-ANALYTICS"}],
            "Period": 60,
            "Statistics": ["Average"]
        },
        "message_visible": {
            "Namespace": "AWS/SQS",
            "MetricName": "ApproximateNumberOfMessagesVisible",
            "Dimensions": [{"Name": "QueueName", "Value": "**"}],
            "Period": 60,
            "Statistics": ["Average"]
        }
    }
}
def format_large_number(value):
    if value >= 1000:
        return f"{value / 1000:.1f}K"
    return f"{value:.0f}"

def fetch_metric_with_window(metric, start_time, end_time, period):
    """Generic function to fetch CloudWatch metrics with specified time window and period."""
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=metric["Namespace"],
            MetricName=metric["MetricName"],
            Dimensions=metric["Dimensions"],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=metric["Statistics"]
        )
        return response if response and response.get("Datapoints") else None
    except Exception:
        return None

def fetch_metric_attempts(metric, is_specific_hourly_metric=False, is_priority_metric=False):
    """
    Fetch the metric with different windows:
    - If is_priority_metric (Request_Count or HTTP_2XX), first try a 1-minute window.
    - If 1-minute returns zero, try a 3-minute window.
    - For others, or if specific hourly, follow their logic.
    """

    end_time = datetime.utcnow()

    if is_specific_hourly_metric:
        # 1-hour window
        start_time = end_time - timedelta(hours=1)
        period = 3600
        response = fetch_metric_with_window(metric, start_time, end_time, period)
        return response, 3600, "hourly"
    elif is_priority_metric:
        # First attempt: 1-minute window
        start_time_1m = end_time - timedelta(minutes=1)
        period_1m = 60
        response_1m = fetch_metric_with_window(metric, start_time_1m, end_time, period_1m)

        # Check if we got a non-zero result
        if response_1m and response_1m.get("Datapoints"):
            # Got data with 1-minute window
            return response_1m, 60, "1-minute"
        else:
            # No data in 1-minute window, try 3-minute window
            start_time_3m = end_time - timedelta(minutes=3)
            period_3m = 180
            response_3m = fetch_metric_with_window(metric, start_time_3m, end_time, period_3m)
            return response_3m, 180, "3-minute-fallback"
    else:
        # Default: 5-minute window
        start_time = end_time - timedelta(minutes=5)
        period = metric["Period"]
        response = fetch_metric_with_window(metric, start_time, end_time, period)
        return response, period, "default"

def get_metrics(metrics_config):
    try:
        end_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
        message = f"Date - {end_time.strftime('%d/%m/%y')}\nHubble Hourly Updates (Production): {end_time.strftime('%I:%M %p')}\n\n"

        efs_size_message = fetch_efs_metric_message()
        message += f"{efs_size_message}\n"

        hubble_sid_message = fetch_hubble_sid_message()
        message += f"{hubble_sid_message}\n"
        message += f"Staging SID = {staging_sid}\n"
        message += f"BT SID = {bt_sid}\n"
        message += f"BT SMS SPENT = ${bt_sms}\n\n"

        for section, metrics in metrics_config.items():
            section_title = section.replace("SmartAnalytics", "Smart Analytics").replace("udp_memory_utilization_metric", "UDP Memory Utilization")
            message += f"{section_title}\n"

            for metric_name, metric in metrics.items():
                is_specific_hourly_metric = (
                    (section == "SERVER1" and metric_name in ["HTTP_5XX", "ELB_5XX"]) or
                    (section == "SERVER2" and metric_name in ["HTTP_3XX", "HTTP_5XX"]) or
                    (section == "SERVER3" and metric_name in ["HTTP_5XX"])
                )

                is_priority_metric = metric_name in ["Request_Count", "HTTP_2XX"]

                response, period, window_type = fetch_metric_attempts(
                    metric,
                    is_specific_hourly_metric=is_specific_hourly_metric,
                    is_priority_metric=is_priority_metric
                )

                if metric_name.startswith("HTTP_") or metric_name.startswith("ELB_"):
                    label = metric_name.replace('_', ' ').upper()
                else:
                    label = metric_name.replace('_', ' ').title()

                if response and response.get("Datapoints"):
                    statistic = metric["Statistics"][0]
                    if statistic == "Average":
                        values = [dp.get("Average", 0) for dp in response["Datapoints"]]
                        value = sum(values) / len(values)
                        if metric_name == "latency":
                            value_ms = value * 1000
                            message += f"Latency = {value_ms:.1f}ms\n"
                        else:
                            message += f"{label} = {int(value)}\n"
                    elif statistic == "Sum":
                        latest_datapoint = max(response["Datapoints"], key=lambda x: x["Timestamp"])
                        value = latest_datapoint.get("Sum", 0)

                        if is_priority_metric and window_type == "3-minute-fallback" and value != 0:
                            value = value / 3

                        if metric_name in ["Request_Count", "HTTP_2XX", "message_visible"]:
                            formatted_value = format_large_number(value)
                        else:
                            formatted_value = str(int(value))
                        message += f"{label} = {formatted_value}\n"
                else:
                    message += f"{label} = 0\n"

            if section == "SERVER3":
                # Add the SERVER3 Memory Utilization
                SERVER3_memory_message = fetch_SERVER3_memory_utilization()
                message += f"{SERVER3_memory_message}\n"

            message += "\n"

        udp_memory = fetch_udp_memory_utilization()
        message += f"UDP Memory Utilization = {udp_memory}\n"

        return message

    except Exception as e:
        return f"Error fetching metrics: {str(e)}"


message = get_metrics(metrics_config)
if __name__ == "__main__":
    time.sleep(30)

    metrics_message = get_metrics(metrics_config)
    print(metrics_message)