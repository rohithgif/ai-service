FROM public.ecr.aws/lambda/python:3.11

# Lambda's task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements
COPY ../../../../requirements.txt .

# Install Python packages
RUN pip install -r requirements.txt

# Copy app.py and embedding code
COPY app.py .
COPY ../../embeddings/code_bert_embeddings.py ./ai_service/embeddings/code_bert_embeddings.py
COPY ../utils/logger.py ./utils/logger.py

# Create necessary directories
RUN mkdir -p ./ai_service/embeddings ./utils

# Download CodeBERT model at build time
RUN mkdir -p ./codebert_model && \
    python -c "from transformers import AutoTokenizer, AutoModel; \
               AutoTokenizer.from_pretrained('microsoft/codebert-base').save_pretrained('./codebert_model'); \
               AutoModel.from_pretrained('microsoft/codebert-base').save_pretrained('./codebert_model')"

# Lambda handler
CMD ["app.handler"]
