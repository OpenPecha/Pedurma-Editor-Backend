import argparse
import os
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError

DATA_PATH = Path(__file__).parent.parent / "data"

os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "~/.aws/op_credentials"


import boto3
from botocore.exceptions import ClientError, NoCredentialsError


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

    # Create S3 client
    s3_client = boto3.client("s3", region_name="ap-south-1")

    # Check if the file already exists
    try:
        s3_client.head_object(Bucket=bucket, Key=object_name)
        # If the above call succeeds, the file already exists.
        print("File already exists in S3. Skipping upload.")
        return False
    except ClientError as e:
        # If a ClientError is thrown, check if it was a 404 error, which means the object does not exist.
        if e.response["Error"]["Code"] == "404":
            # The file does not exist and can be uploaded.
            try:
                s3_client.upload_file(file_name, bucket, object_name)
                return True
            except NoCredentialsError:
                print("Credentials not available")
                return False
        else:
            # Some other error occurred.
            print(f"Unexpected error: {e}")
            return False


def get_volumes_mappings(pecha: Path) -> dict[str, str]:
    mappings_fn = DATA_PATH / "mappings" / f"{pecha}.txt"
    volumes = [vol for vol in mappings_fn.read_text().splitlines() if vol]
    mappings = {}
    for i, vol in enumerate(volumes):
        mappings[vol] = f"v{i+1:03}"
    return mappings


def upload_images(images_path: Path, pecha: str, volume_name: str):

    for image_fn in sorted(images_path.iterdir()):
        image_num = image_fn.stem[-4:]
        if int(image_num) < 3:
            continue
        print(f"[INFO] uploading {pecha}/{volume_name}/{image_num}")
        s3_object_name = f"{pecha}/{volume_name}/{image_num}.{image_fn.suffix}"
        upload_to_s3(str(image_fn), "pedurma", object_name=s3_object_name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("images_path", help="images to be uploaded")
    ap.add_argument("pecha", help="kangyur or tengyur")

    args = ap.parse_args()

    mappings = get_volumes_mappings(args.pecha)
    images_path = Path(args.images_path)
    volume_name = mappings[images_path.name]
    upload_images(images_path, args.pecha, volume_name)


# Upload the image
# if upload_to_s3(file_name, bucket_name, object_name=object_name):
#     print(f"'{file_name}' has been uploaded to '{bucket_name}'.")
# else:
#     print("Upload failed.")
