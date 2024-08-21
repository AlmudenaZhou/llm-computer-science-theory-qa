from abc import ABC
import logging
from typing import Any


logger = logging.getLogger(__name__)

class BaseOpenAIClient(ABC):

    client: Any
    model_name: str

    def completion(self, start_phrase, model_name=None, **kwargs):

        model_name = model_name if model_name else self.model_name
        response = self.client.completions.create(model=model_name, prompt=start_phrase, **kwargs)
        logger.info(start_phrase + response.choices[0].text)
        return response
    
    def chat(self, messages, model_name=None, **kwargs):
        """
        messages must have the following structure: 
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
            {"role": "user", "content": "Do other Azure AI services support this too?"}
        ]
        It will respond to the last user role
        """
        model_name = model_name if model_name else self.model_name
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages, 
            **kwargs
        )

        logger.info(response.choices[0].message.content)
        return response
