import os
import jinja2

from src.client_modules.utils import import_openai_llms


class Generation:

    def __init__(self, llm_client=None, prompt_template_path=os.getenv("GENERATION_TEMPLATE_PATH", "templates/")) -> None:
        self.llm_client = llm_client if not None else import_openai_llms("ollama")()
        self.prompt_template_path = prompt_template_path

    def load_prompt(self, prompt_template_name):
        templateLoader = jinja2.FileSystemLoader(searchpath=self.prompt_template_path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(prompt_template_name)
        return template

    def build_chat_prompt(self, user_query, search_results):

        template = self.load_prompt("chat_generation_prompt.txt")
        context = "\n\n".join(
            [
                f"question: {doc['_source']['questions_vector_text']}\nanswer: {doc['_source']['answers_vector_text']}"
                for doc in search_results
            ]
        )
        return template.render(question=user_query, context=context).strip()
    
    def build_evaluation_prompt(self, user_query, answer):
        template = self.load_prompt("evaluation_prompt.txt")
        return template.render(question=user_query, answer=answer).strip()
    
    def generate_response_from_prompt(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        return self.llm_client.chat(messages, temperature=0.0)
