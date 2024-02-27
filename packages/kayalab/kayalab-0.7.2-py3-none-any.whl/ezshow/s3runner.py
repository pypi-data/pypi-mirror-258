from minio import Minio
from minio.error import S3Error

from nicegui import app

appstore = app.storage.general["demo"]


# https://github.com/minio/minio-py
# file_uploader.py MinIO Python SDK example
def upload():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        appstore["host"],
        access_key="",
        secret_key="",
    )

    # Create bucket.
    client.make_bucket("my-bucket")

    # The file to upload, change this path if needed
    source_file = "/tmp/test-file.txt"

    # The destination bucket and filename on the MinIO server
    bucket_name = "python-test-bucket"
    destination_file = "my-test-file.txt"

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(
        bucket_name,
        destination_file,
        source_file,
    )
    print(
        source_file,
        "successfully uploaded as object",
        destination_file,
        "to bucket",
        bucket_name,
    )

