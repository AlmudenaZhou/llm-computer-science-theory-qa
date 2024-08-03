import os
import logging

from openai import OpenAI

from modules.llms.openai.base import BaseOpenAIClient


logger = logging.getLogger(__name__)

class OpenAIClient(BaseOpenAIClient):

    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI(
                api_key=os.getenv("OPENAI_TOKEN"),
            )

        self.model_name = os.getenv("OPENAI_MODEL")
