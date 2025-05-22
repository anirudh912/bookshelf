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

def download_from_s3(bucket_name, object_name, file_path, profile='books'):
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')
    try:
        s3.download_file(bucket_name, object_name, file_path)
        print("Successfully downloaded the file from S3 bucket.")
    except Exception as e:
        print(f"Failed to download file: {e}")
        raise

def list_files_in_s3(bucket_name, profile='books'):
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except Exception as e:
        print(f"Failed to list files: {e}")
        return []

def delete_file_from_s3(bucket_name, object_name, profile='books'):
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print("Successfully deleted the file from S3 bucket.")
    except Exception as e:
        print(f"Failed to delete file: {e}")
        raise