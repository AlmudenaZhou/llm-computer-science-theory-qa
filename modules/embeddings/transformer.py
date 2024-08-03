import os

from sentence_transformers import SentenceTransformer

from modules.embeddings.base import AbstractEmbeddingModel


class TransformerEmbeddingModel(AbstractEmbeddingModel):

    def __init__(self) -> None:
        super().__init__()
        self.model_name = os.getenv("TRANSFORMER_EMB_MODEL_NAME")
        self.client = SentenceTransformer(self.model_name)

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []

        for chunk in chunks:

            embeddings_batch = self.client.encode([chunk])
            if len(embeddings_batch[0]) == 768:
                embeddings.extend(embeddings_batch)
            else:
                raise ValueError

        return embeddings
