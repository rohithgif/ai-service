import json
from langchain.vectorstores import FAISS
from ai_service.embeddings.code_bert_embeddings import CodeBERTEmbeddings
import boto3
from langchain.llms.bedrock import Bedrock
import traceback
from utils.logger import setup_logger

logger = setup_logger('exception_answering_ai')
s3 = boto3.client('s3')

def handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        exception_text = event.get('exception', '')
        if not exception_text:
            logger.warning("No exception text provided in the request")
            return {"statusCode": 400, "body": "No exception text provided"}

        logger.info("Initializing CodeBERT embeddings")
        embedder = CodeBERTEmbeddings()
        
        logger.info("Downloading FAISS index from S3")
        s3.download_file('grabhackbucket', 'faiss/index.faiss', '/tmp/index.faiss')
        
        logger.info("Loading FAISS index")
        vectorstore = FAISS.load_local("/tmp/index.faiss", embedder)

        logger.info("Performing similarity search")
        docs = vectorstore.similarity_search(exception_text, k=3)
        context_str = "\n".join([doc.page_content for doc in docs])
        logger.debug(f"Found context: {context_str}")

        logger.info("Initializing Bedrock client")
        llm = Bedrock(model_id="anthropic.claude-v2")
        
        logger.info("Generating explanation with Bedrock")
        prompt = f"Exception: {exception_text}\nContext:\n{context_str}\nExplain why this is happening."
        answer = llm.invoke(prompt)
        logger.info("Successfully generated explanation")
        logger.debug(f"Generated answer: {answer}")

        return {
            "statusCode": 200,
            "body": answer
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }
