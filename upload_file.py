import boto3
import os

def upload_to_s3(file_path, bucket_name, object_name, profile='books'):
    session = boto3.Session(profile_name=profile)
    s3= session.client('s3')
    if not os.path.exists(file_path):
        print("File does not exist.")
        return
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print("Successfully uploaded the file to S3 bucket.")
    except Exception as e:
        print(f"Failed to upload file: {e}")
        raise