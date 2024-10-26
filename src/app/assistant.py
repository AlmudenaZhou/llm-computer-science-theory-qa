import os
import time
import json

from src.client_modules.utils import import_embeddings, import_openai_llms
from src.app.generation import Generation
from src.app.retrieval import Retrieval


def format_llm_answer(response):
    answer = response.choices[0].message.content
    tokens = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens
    }
    return answer, tokens


def rag_workflow(query, llm_client):
    embedding_client = os.getenv("EMBEDDING_CLIENT")
    embedding_client = import_embeddings(embedding_client)()
    retrieval_inst = Retrieval(embedding_client=embedding_client)
    search_results = retrieval_inst.search_from_text(query)
    print("------------ Search Results ------------")
    print(search_results)

    generation_inst = Generation(llm_client=llm_client)
    prompt = generation_inst.build_chat_prompt(query, search_results)
    print("------------ Prompt ------------")
    print(prompt)
    response = generation_inst.generate_response_from_prompt(prompt)
    print("------------ Response ------------")
    print(response)
    return response


def llm(query, llm_client):
    start_time = time.time()

    response = rag_workflow(query, llm_client)

    end_time = time.time()
    response_time = end_time - start_time

    answer, tokens = format_llm_answer(response)
    
    return answer, tokens, response_time


def evaluate_relevance(query, answer, llm_client):
    generation_inst = Generation(llm_client=llm_client)
    prompt = generation_inst.build_evaluation_prompt(query, answer)
    response = generation_inst.generate_response_from_prompt(prompt)

    evaluation, tokens = format_llm_answer(response)
    try:
        json_eval = json.loads(evaluation)
        return json_eval['Relevance'], json_eval['Explanation'], tokens
    except json.JSONDecodeError:
        return "UNKNOWN", "Failed to parse evaluation", tokens


def calculate_openai_cost(model_choice, tokens):
    openai_cost = 0

    if model_choice == 'openai/gpt-3.5-turbo':
        openai_cost = (tokens['prompt_tokens'] * 0.0015 + tokens['completion_tokens'] * 0.002) / 1000
    elif model_choice in ['openai/gpt-4o', 'openai/gpt-4o-mini']:
        openai_cost = (tokens['prompt_tokens'] * 0.03 + tokens['completion_tokens'] * 0.06) / 1000

    return openai_cost


def get_answer(query, model_choice):

    llm_client_name, llm_model_name = model_choice.split('/')
    llm_client_name = "azure_openai" if llm_client_name == "openai" else llm_client_name

    if llm_client_name not in ["azure_openai", "ollama"]:
        raise ValueError(f"Unknown model choice: {model_choice}")
    
    llm_client = import_openai_llms(llm_client_name)(model_name=llm_model_name)

    answer, tokens, response_time = llm(query, llm_client)
    
    relevance, explanation, eval_tokens = evaluate_relevance(query, answer, llm_client)

    openai_cost = calculate_openai_cost(model_choice, tokens)
 
    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': model_choice,
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'eval_prompt_tokens': eval_tokens['prompt_tokens'],
        'eval_completion_tokens': eval_tokens['completion_tokens'],
        'eval_total_tokens': eval_tokens['total_tokens'],
        'openai_cost': openai_cost
    }
