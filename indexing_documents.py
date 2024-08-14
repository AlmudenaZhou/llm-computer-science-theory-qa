import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from modules.embeddings.transformer import TransformerEmbeddingModel
from modules.elastic_search.elastic_search_client import ElasticSearchClient


load_dotenv()


class IndexDocuments:

    def __init__(self) -> None:
        pass

def read_data():
        with open("data/intents.json") as file:
            intents = json.load(file)["intents"]

        return intents


def calc_embed_from_intents(intents):

    emb_model = TransformerEmbeddingModel()

    embedding_text_template = ("""Equivalent questions: \"""{patterns}\"""
    Equivalent answers:\"""{responses}\"""
    """)


    for intent in tqdm(intents):
        embedding_text = embedding_text_template.format(
            patterns='\n- '.join(intent["patterns"]),
            responses='\n- '.join(intent["responses"])
        )
        intent['text'] = embedding_text
        intent['vector_field'] = emb_model.get_embeddings([embedding_text])[0].tolist()

    return intents


def add_documents_to_index(intents, es_client, index_name):

    try:
        es_client.index_documents(index_name=index_name, documents=intents)
    except Exception as e:
        print(e)


def main_indexing_workflow(index_settings, index_name):
    intents = read_data()
    intents = calc_embed_from_intents(intents)

    es_client = ElasticSearchClient()

    force_recreate = os.getenv("ELASTICSEARCH_FORCE_RECREATE", "False") == "True"

    if force_recreate:
        es_client.delete_index(index_name)

    if not es_client.index_exists(index_name):
        es_client.create_index(index_name=index_name, index_settings=index_settings)

    add_documents_to_index(intents, es_client, index_name)



def main():

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "tag": {"type": "text"},
                "patterns": {"type": "text"},
                "responses": {"type": "text"},
                "text": {"type": "text"} ,
                "vector_field": {"type": "dense_vector", "dims": 768,
                                 "index": True, "similarity": "cosine"},
            }
        }
    }
    index_name = os.getenv("ELASTICSEARCH_INDEX_NAME", "cs-theory")

    main_indexing_workflow(index_settings, index_name)

if __name__ == '__main__':
    main_indexing_workflow()
