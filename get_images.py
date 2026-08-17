import boto3

ecr_client = boto3.client(
    "ecr",
    region_name="eu-west-3"
)

response = ecr_client.describe_images(
    repositoryName="automation-with-python"
)

images = response["imageDetails"]

for image in images:
    if "imageTags" in image:
        for tag in image["imageTags"]:
            print(tag)