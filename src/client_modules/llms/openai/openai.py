import os
import logging

from openai import OpenAI

from src.client_modules.llms.openai.base import BaseOpenAIClient


logger = logging.getLogger(__name__)

class OpenAIClient(BaseOpenAIClient):

    def __init__(self, model_name=os.getenv("OPENAI_MODEL")) -> None:
        super().__init__()
        self.client = OpenAI(
                api_key=os.getenv("OPENAI_TOKEN"),
            )

        self.model_name = model_name
