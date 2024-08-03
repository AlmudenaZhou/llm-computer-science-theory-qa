import os
import logging

from openai import OpenAI

from modules.llms.openai.base import BaseOpenAIClient


logger = logging.getLogger(__name__)

class OllamaClient(BaseOpenAIClient):

    def __init__(self) -> None:
        super().__init__()
        
        self.client = OpenAI(
                base_url='http://localhost:11434/v1/',
                api_key="ollama",
            )
            
        self.model_name = os.getenv("OLLAMA_MODEL")
