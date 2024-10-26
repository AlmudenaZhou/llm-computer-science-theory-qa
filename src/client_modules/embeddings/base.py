from abc import ABC
from typing import Any


class AbstractEmbeddingModel(ABC):

    client: Any
    model_name: str
    _model_dimensions: dict

    def get_model_dimension(self) -> int:
        if self.model_name not in self._model_dimensions:
            raise NotImplementedError(f"{self.model_name} is not implemented in _model_dimensions of {self.__repr__}")
        return self._model_dimensions[self.model_name]

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        pass
