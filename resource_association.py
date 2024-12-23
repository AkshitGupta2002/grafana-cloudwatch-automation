import boto3

def get_security_group_associations(security_group_ids):
    """
    List resources associated with a given list of security group IDs.
    """
    ec2_client = boto3.client('ec2')
    elbv2_client = boto3.client('elbv2')

    result = {}

    for sg_id in security_group_ids:
        result[sg_id] = []

        # Check associated EC2 instances
        instances_response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance.group-id', 'Values': [sg_id]}]
        )
        for reservation in instances_response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                result[sg_id].append({
                    "ResourceType": "EC2 Instance",
                    "ResourceName": instance.get('Tags', [{'Key': 'Name', 'Value': 'Unnamed'}])[0]['Value'],
                    "ResourceId": instance['InstanceId']
                })

        # Check associated network interfaces
        interfaces_response = ec2_client.describe_network_interfaces(
            Filters=[{'Name': 'group-id', 'Values': [sg_id]}]
        )
        for interface in interfaces_response.get('NetworkInterfaces', []):
            result[sg_id].append({
                "ResourceType": "Network Interface",
                "ResourceName": interface.get('Description', 'Unnamed Interface'),
                "ResourceId": interface['NetworkInterfaceId']
            })

        # Check associated load balancers (ELBv2)
        load_balancers_response = elbv2_client.describe_load_balancers()
        for lb in load_balancers_response.get('LoadBalancers', []):
            if sg_id in lb.get('SecurityGroups', []):
                result[sg_id].append({
                    "ResourceType": "Load Balancer",
                    "ResourceName": lb.get('LoadBalancerName', 'Unnamed Load Balancer'),
                    "ResourceId": lb.get('LoadBalancerArn', 'Unknown ARN')
                })

        # If no associations are found
        if not result[sg_id]:
            result[sg_id].append("No association")

    return result


def main():
    # Replace with the security group IDs from the Custodian mail
    security_group_ids = [
        "sg-2418316e",
        "sg-005f71754530d97a5",
        "sg-0576c4af37446a361",
        "sg-076ab11246e913f91",
        "sg-9a8d5de5",
        "sg-03354f71b3596510e",
        "sg-0754c6f01ef77f1bf",
        "sg-0ddde8a008e12cdf3",
        "sg-04e2711617402a01b",
        "sg-251c4958"
    ]

    associations = get_security_group_associations(security_group_ids)

    for sg_id, resources in associations.items():
        print(f"Security Group: {sg_id}")
        for resource in resources:
            if isinstance(resource, str):  # No association
                print(f"  - {resource}")
            else:
                print(f"  - Resource Type: {resource['ResourceType']}")
                print(f"    Resource Name: {resource['ResourceName']}")
                print(f"    Resource ID: {resource['ResourceId']}")
        print()  # Add a blank line between security groups


if __name__ == "__main__":
    main()
