import os

from openai import AzureOpenAI

from src.client_modules.embeddings.base import AbstractEmbeddingModel


class AzureOpenAIEmbeddingModel(AbstractEmbeddingModel):

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
        for chunk in chunks:

            response = self.client.embeddings.create(
                input=chunk,
                model=self.model_name,
            )

            print(response.model_dump_json(indent=2))

            embeddings_batch = [res_data.embedding for res_data in response.data]

            if len(embeddings_batch[0]) == 1536:
                embeddings.extend(embeddings_batch)
            else:
                raise ValueError

        return embeddings
