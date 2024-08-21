import os
import logging

from openai import AzureOpenAI

from src.client_modules.llms.openai.base import BaseOpenAIClient


logger = logging.getLogger(__name__)

class AzureOpenAIClient(BaseOpenAIClient):

    def __init__(self) -> None:
        super().__init__()
        self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            
        self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        logger.info("Instantiated AzureOpenAI client")