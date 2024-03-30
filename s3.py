import boto3
from botocore.exceptions import NoCredentialsError


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client("s3", region_name="ap-south-1")
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except NoCredentialsError:
        print("Credentials not available")
        return None

    return presigned_url


# Example usage
object_name = "W1PD95844/I1PD95846/I1PD958461520.jpg"
bucket_name = "pedurma"  # Specify your S3 bucket name
expiration = 600  # Presigned URL expiry time in seconds

# Generate a presigned URL
url = create_presigned_url(bucket_name, object_name, expiration)
if url:
    print(f"Presigned URL: {url}")
else:
    print("Failed to generate presigned URL.")
