FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

COPY ../../../../requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .
COPY ../../embeddings/code_bert_embeddings.py ./ai_service/embeddings/code_bert_embeddings.py
COPY ../utils/logger.py ./utils/logger.py

RUN mkdir -p ./ai_service/embeddings ./utils

RUN mkdir -p ./codebert_model && \
    python -c "from transformers import AutoTokenizer, AutoModel; \
               AutoTokenizer.from_pretrained('microsoft/codebert-base').save_pretrained('./codebert_model'); \
               AutoModel.from_pretrained('microsoft/codebert-base').save_pretrained('./codebert_model')"

CMD ["app.handler"]
