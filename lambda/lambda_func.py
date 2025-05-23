import boto3
import json
import time

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    textract = boto3.client('textract')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bookshelf-text')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        response = textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        job_id = response['JobId']
        while True:
            status = textract.get_document_text_detection(JobId=job_id)
            if status['JobStatus'] in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(5)
        if status['JobStatus'] == 'SUCCEEDED':
            text = []
            next_token = None
            while True:
                if next_token:
                    response = textract.get_document_text_detection(
                        JobId=job_id, NextToken=next_token
                    )
                else:
                    response = textract.get_document_text_detection(JobId=job_id)
                for item in response['Blocks']:
                    if item['BlockType'] == 'LINE':
                        text.append(item['Text'])
                next_token = response.get('NextToken')
                if not next_token:
                    break
            extracted_text = " ".join(text)
            table.put_item(
                Item={
                    'doc_id': key,
                    'text': extracted_text,
                    'bucket': bucket
                }
            )
            print("Text extracted and stored!")
        else:
            print(f"Textract job failed: {status['JobStatus']}")

    except Exception as e:
        print(f"Error processing {key}: {str(e)}")
        raise
