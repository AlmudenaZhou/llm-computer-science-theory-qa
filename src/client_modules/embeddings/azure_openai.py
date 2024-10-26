import os
import logging

from openai import AzureOpenAI

from src.client_modules.embeddings.base import AbstractEmbeddingModel

logger = logging.getLogger(__name__)


class AzureOpenAIEmbeddingModel(AbstractEmbeddingModel):

    _model_dimensions = {"text-embedding-ada-002": 1536}
    _model_max_context = {"text-embedding-ada-002": 8191}

    def __init__(self) -> None:
        super().__init__()
        self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            
        self.model_name = os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME")

    def get_embeddings(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []

        model_dim = self.get_model_dimension()

        for chunk in chunks:

            response = self.client.embeddings.create(
                input=chunk,
                model=self.model_name,
            )

            logger.debug(response.model_dump_json(indent=2))

            embeddings_batch = [res_data.embedding for res_data in response.data]

            if len(embeddings_batch[0]) == model_dim:
                embeddings.extend(embeddings_batch)
            else:
                raise ValueError(f"Dimensions from {self.model_name} expected to be {model_dim}")

        return embeddings
