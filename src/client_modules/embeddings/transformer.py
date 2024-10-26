import os

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

from src.client_modules.embeddings.base import AbstractEmbeddingModel


class TransformerEmbeddingModel(AbstractEmbeddingModel):

    _model_dimensions = {"distilbert-base-nli-mean-tokens": 768}
    _model_max_context = {"distilbert-base-nli-mean-tokens": 100_000}

    def __init__(self) -> None:
        super().__init__()
        self.model_name = os.getenv("TRANSFORMER_EMB_MODEL_NAME")
        self.client = SentenceTransformer(self.model_name)

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []

        model_dim = self.get_model_dimension()

        for chunk in chunks:

            embeddings_batch = self.client.encode([chunk])
            if len(embeddings_batch[0]) == model_dim:
                embeddings.extend(embeddings_batch)
            else:
                raise ValueError(f"Dimensions from {self.model_name} expected to be {model_dim}")
        return embeddings
    
    def get_encoded_input(self, text):
        tokenizer = AutoTokenizer.from_pretrained(f'sentence-transformers/{self.model_name}')
        full_response = tokenizer(text)
        encoded_input = full_response['input_ids']
        return encoded_input, full_response

    def get_text_num_tokens(self, text):
        encoded_input, _ = self.get_encoded_input(text)
        return len(encoded_input)
