from abc import ABC
from typing import Any


class AbstractEmbeddingModel(ABC):

    client: Any
    model_name: str

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        pass
