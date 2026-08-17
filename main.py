from sys import deactivate_stack_trampoline

import boto3
import requests
import time

#Exercise 1: Working with Subnets in AWS
"""

ec2 = boto3.client('ec2', region_name='eu-west-3')
subnets = ec2.describe_subnets()
for sub in subnets['Subnets']:
    print(sub['SubnetId'])
"""

""" 
# EXERCISE 2: Working with IAM in AWS


client = boto3.client('iam')
response = client.list_users()
for user in response['Users']:
    print("Username:", user['UserName'])
    print("Password last used:", user.get('PasswordLastUsed', 'Never used'))

# Print out the user ID and name of the user who was active the most recently
response = client.list_users()

most_recent_user = None
most_recent_date = None

for user in response["Users"]:
    last_used = user.get("PasswordLastUsed")
    # Only check users who have PasswordLastUsed
    if last_used:
        if most_recent_date is None or last_used > most_recent_date:
            most_recent_date = last_used
            most_recent_user = user
if most_recent_user:
    print("User ID:", most_recent_user["UserId"])
    print("User Name:", most_recent_user["UserName"])
    print("Last Active:", most_recent_date)
else:
    print("No users have password activity.")
"""


"""
# EXERCISE 3: Automate Running and Monitoring Application on EC2 instance

ec2_client = boto3.client('ec2', region_name='eu-west-3')

response = ec2_client.describe_vpcs(
    Filters=[
        {
            "Name": "is-default",
            "Values": ["true"]
        }
    ]
)
default_vpc_id = response["Vpcs"][0]["VpcId"]

print("Default VPC:", default_vpc_id)

subnet_response = ec2_client.describe_subnets(
    Filters=[
        {
            "Name": "vpc-id",
            "Values": [default_vpc_id]
        },
        {
            "Name": "default-for-az",
            "Values": ["true"]
        }
    ]
)

subnet_id = subnet_response["Subnets"][0]["SubnetId"]

print("Subnet:", subnet_id)

response = ec2_client.run_instances(
    ImageId="ami-03dbc12aeff16b2d4",
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1,
    SubnetId=subnet_id,
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "nginx-server"
                }
            ]
        }
    ]
)

instance_id = response["Instances"][0]["InstanceId"]

# Create a scheduled function that sends a request to the nginx application and checks the status is OK

import subprocess

NGINX_URL = "http://13.38.53.59"

failed_count = 0

def monitor_website():
    try:
        response = requests.get(NGINX_URL, timeout=5)

        if response.status_code == 200:
            print("Application is running OK")
            return True
        else:
            print("Application is not OK")
            return False

    except requests.RequestException:
        print("Application is not reachable")
        return False


def restart_nginx():
    print("Restarting Nginx...")

    subprocess.run(
        ["docker", "restart", "nginx"],
        check=True
    )


# Run monitoring continuously
while True:
    status = monitor_website()

    if status:
        failed_count = 0
    else:
        failed_count += 1

    print("Failed count:", failed_count)

    if failed_count >= 5:
        restart_nginx()
        failed_count = 0

    time.sleep(60)
    break

"""

# EXERCISE 4: Working with ECR in AWS

""" 
import boto3

ecr_client = boto3.client("ecr", region_name="eu-west-3")

# 1. Get all repositories
response = ecr_client.describe_repositories()

repositories = response["repositories"]

# 2. Print repository names
print("ECR Repositories:")

for repo in repositories:
    print(repo["repositoryName"])


# 3. Choose one repository
repository_name = "automation-with-python"

images_response = ecr_client.describe_images(
    repositoryName=repository_name
)

images = images_response["imageDetails"]


# Keep only images that have tags
images_with_tags = []

for image in images:
    if "imageTags" in image:
        images_with_tags.append(image)


# Sort by push date, newest first
images_with_tags.sort(
    key=lambda image: image["imagePushedAt"],
    reverse=True
)


# Print image tags
print("\nImage tags:")

for image in images_with_tags:
    print(
        image["imageTags"],
        image["imagePushedAt"]
    )
"""

#5 EXERCISE 5: Python in Jenkins Pipeline

# Fetch all 3 images from the ECR repository (using Python)

ecr_client = boto3.client('ecr', region_name='eu-west-3')

response = ecr_client.describe_images( repositoryName='automation-with-python')
# print(response["imageDetails"])

images = response["imageDetails"]
for image in images:
    if "imageTags" in image:
        print(image["imageTags"])

# Let the user select the image from the list (hint: https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/)

