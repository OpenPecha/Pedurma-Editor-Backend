import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3", region_name="ap-south-1")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True


# Example usage
file_name = (
    "data/W1PD95844/I1PD95846/I1PD958461520.jpg"  # Specify the path to your image
)
object_name = "W1PD95844/I1PD95846/I1PD958461520.jpg"
bucket_name = "pedurma"  # Specify your S3 bucket name

# Upload the image
if upload_to_s3(file_name, bucket_name, object_name=object_name):
    print(f"'{file_name}' has been uploaded to '{bucket_name}'.")
else:
    print("Upload failed.")
