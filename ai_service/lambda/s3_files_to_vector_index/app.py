from langchain.vectorstores import FAISS
from ai_service.embeddings.code_bert_embeddings import CodeBERTEmbeddings
import boto3
import os
import json
import traceback
from utils.logger import setup_logger

logger = setup_logger('s3_files_to_vector_index')
s3 = boto3.client('s3')

def handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        bucket = "grabhackbucket"
        prefix = "projects/"
        logger.info(f"Processing files from bucket: {bucket}, prefix: {prefix}")
        
        logger.info("Initializing CodeBERT embeddings")
        embedder = CodeBERTEmbeddings()
        vectorstore = None
        keys = []

        logger.info("Starting file processing")
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get('Contents', []):
                key = obj['Key']
                if not key.endswith('/'):
                    logger.info(f"Processing file: {key}")
                    data = s3.get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf-8')
                    
                    if vectorstore is None:
                        logger.info("Creating new FAISS index")
                        vectorstore = FAISS.from_texts([data], embedder, metadatas=[{"key": key}])
                    else:
                        logger.info("Adding to existing FAISS index")
                        vectorstore.add_texts([data], metadatas=[{"key": key}])
                    keys.append(key)
                    logger.info(f"Successfully processed file: {key}")

        if not keys:
            logger.warning("No files found to process")
            return {"statusCode": 200, "body": "No files found to process"}

        logger.info("Creating temporary directory for vector DB")
        os.makedirs("/tmp/vector_db/faiss_index", exist_ok=True)
        
        logger.info("Saving FAISS index locally")
        vectorstore.save_local("/tmp/vector_db/faiss_index")
        
        logger.info("Uploading FAISS index to S3")
        s3.upload_file("/tmp/vector_db/faiss_index/index.faiss", bucket, "vector_db/index.faiss")
        
        message = f"Successfully indexed {len(keys)} files"
        logger.info(message)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": message,
                "indexed_files": keys
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }
