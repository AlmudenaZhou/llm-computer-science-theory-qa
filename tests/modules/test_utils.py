import sys, os

sys.path.append(os.getcwd())

from src.client_modules.embeddings.azure_openai import AzureOpenAIEmbeddingModel
from src.client_modules.embeddings.transformer import TransformerEmbeddingModel
from src.client_modules.llms.openai.azure_openai import AzureOpenAIClient
from src.client_modules.llms.openai.ollama import OllamaClient
from src.client_modules.llms.openai.openai import OpenAIClient
from src.client_modules.utils import import_embeddings, import_openai_llms, get_parent_folders_inside_project


def test_import_embeddings():
    assert import_embeddings("transformer") == TransformerEmbeddingModel
    assert import_embeddings("azure_openai") == AzureOpenAIEmbeddingModel


def test_import_llms():
    assert import_openai_llms("ollama") == OllamaClient
    assert import_openai_llms("azure_openai") == AzureOpenAIClient
    assert import_openai_llms("openai") == OpenAIClient


def test_get_parent_folders_inside_project():
    parent_folders = get_parent_folders_inside_project()
    msg = f'get_parent_folders_inside_project() must return ["src", "client_modules"] not {parent_folders}'
    assert parent_folders == ["src", "client_modules"], msg
