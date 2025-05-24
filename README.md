# BookShelf: Smart Document Hub

BookShelf is a document processing and management application built on AWS cloud services, allowing users to upload PDFs and images, automatically extracts text, generates summaries, and enables chat with documents through a simple web interface.

## Features

- **Upload documents** to AWS S3.
- **Automated text extraction** with Amazon Textract.
- **AI-powered summarization** with Amazon Bedrock (Claude 3 Haiku).
- **Store and search** text and summaries in DynamoDB.
- **Web-based UI** for listing, searching, downloading, and chatting with documents.

## Setup

1. **AWS Resources:**
   - S3 bucket for uploads.
   - DynamoDB table for storage.
   - Lambda function with correct IAM role and permissions.
   - Bedrock model access in a supported AWS region.
2. **Local Development:**
   - Install dependencies: `pip install -r requirements.txt`.
   - Set up AWS credentials.
   - Run: `streamlit run app.py`.

## Project Status

The code and setup are complete. Due to regional availability, Amazon Bedrock is not supported in all AWS regions (e.g., ap-south-1). With the correct region you will have access to Bedrock and the app will run as intended.
