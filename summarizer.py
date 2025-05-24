import boto3
import json

def summarize_text_bedrock(text, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
    bedrock = boto3.client('bedrock-runtime')
    prompt = f"Human: Summarize the following document:\n\n{text}\n\nAssistant:"
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 2048,
            "temperature": 0.3
        })
    )
    return json.loads(response['body'].read())['completion']

def chat_with_doc_bedrock(context, question, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
    bedrock = boto3.client('bedrock-runtime')
    prompt = f"Human: Context:\n{context}\n\nQuestion: {question}\n\nAssistant:"
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 1024,
            "temperature": 0.3
        })
    )
    return json.loads(response['body'].read())['completion']
