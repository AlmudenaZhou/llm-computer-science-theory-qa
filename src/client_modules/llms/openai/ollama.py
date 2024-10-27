import os
import logging

from openai import OpenAI

from src.client_modules.llms.openai.base import BaseOpenAIClient


logger = logging.getLogger(__name__)

class OllamaClient(BaseOpenAIClient):

    def __init__(self, model_name=os.getenv("OLLAMA_MODEL"), ollama_url=os.getenv("OLLAMA_URL")) -> None:
        super().__init__()

        self.client = OpenAI(
                base_url=ollama_url,
                api_key="ollama",
            )
            
        self.model_name = model_name
