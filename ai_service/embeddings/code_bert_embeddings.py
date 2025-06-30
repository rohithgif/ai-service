from langchain.embeddings.base import Embeddings
from transformers import AutoTokenizer, AutoModel
import torch

class CodeBERTEmbeddings(Embeddings):
    def __init__(self):
        # Load from local model dir (built into image)
        self.tokenizer = AutoTokenizer.from_pretrained("./codebert_model")
        self.model = AutoModel.from_pretrained("./codebert_model")

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
