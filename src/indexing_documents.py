import os
import sys
import json
import logging
import logging.config
from tqdm import tqdm
from dotenv import load_dotenv

import numpy as np

sys.path.append(os.getcwd())

logging.config.fileConfig('logger.conf')
logger = logging.getLogger(__name__)

from src.client_modules.elastic_search.elastic_search_client import ElasticSearchClient
from src.client_modules.utils import check_embedding_model, import_embeddings, get_embedding_model_name


load_dotenv()


class IndexDocuments:

    def __init__(self, index_settings, 
                 es_client=ElasticSearchClient(),
                 index_name=os.getenv("ELASTICSEARCH_INDEX_NAME", "cs-theory"),
                 embedding_client=os.getenv("EMBEDDING_CLIENT", "transformer"), 
                 force_recreate_index=os.getenv("ELASTICSEARCH_FORCE_RECREATE", 
                                                "False") == "True"
                 ) -> None:
        logger.info(f"Creating index {index_name} with embedding: {embedding_client}")
        self.index_settings = index_settings
        self.index_name = index_name
        self.embedding_client = embedding_client
        self.force_recreate_index = force_recreate_index
        self.es_client = es_client

    @staticmethod
    def read_data():
        with open("data/all_qa_cleaned.json") as file:
            intents = json.load(file)
        return intents

    @staticmethod
    def get_text_embedding(emb_model, embedding_text):
        embedding = emb_model.get_embeddings([embedding_text])[0]
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        return embedding

    def get_combined_qa_text_embedding(self, emb_model, intent):
        embedding_text_template = ("""\"""{patterns}\"""
        \"""{responses}\"""
        """)

        embedding_text = embedding_text_template.format(
            patterns='\n- '.join(intent["patterns"]),
            responses='\n- '.join(intent["responses"])
        )

        embedding = self.get_text_embedding(emb_model, embedding_text)

        return embedding_text, embedding

    def get_questions_embedding(self, emb_model, intent):

        embedding_text = '\n- '.join(intent["patterns"])
        embedding = self.get_text_embedding(emb_model, embedding_text)
        return embedding_text, embedding

    def get_answers_embedding(self, emb_model, intent):

        embedding_text = '\n- '.join(intent["responses"])
        embedding = self.get_text_embedding(emb_model, embedding_text)
        return embedding_text, embedding

    def get_complete_intent_for_indexing(self, emb_model, intent):

        comb_text, comb_embedding = self.get_combined_qa_text_embedding(emb_model, intent)

        intent["comb_qa"] = comb_text
        intent["combined_qa_vector"] = comb_embedding
        print(len(comb_embedding), type(comb_embedding))

        questions_text, questions_embedding = self.get_questions_embedding(emb_model, intent)
        intent["patterns"] = questions_text
        intent["questions_vector"] = questions_embedding

        answers_text, answers_embedding = self.get_answers_embedding(emb_model, intent)
        intent["responses"] = answers_text
        intent["answers_vector"] = answers_embedding

        return intent

    def add_document_to_index(self, intent):

        try:
            self.es_client.index_documents(index_name=self.index_name, documents=[intent])
        except Exception as e:
            print(e)

    def main_indexing_workflow(self):
        intents = self.read_data()
        if self.force_recreate_index:
            self.es_client.delete_index(self.index_name)

        if not self.es_client.index_exists(self.index_name):
            self.es_client.create_index(index_name=self.index_name, 
                                        index_settings=self.index_settings)

        emb_class = import_embeddings(self.embedding_client)
        emb_model = emb_class()

        for intent in tqdm(intents):
            intent = self.get_complete_intent_for_indexing(emb_model, intent)

            self.add_document_to_index(intent)


def main():

    dimension_mapping = {
        "transformer": {"distilbert-base-nli-mean-tokens": 768},
        "azure_openai": {"text-embedding-ada-002": 1536}
    }

    embedding_client = os.getenv("EMBEDDING_CLIENT", "transformer")
    check_embedding_model(embedding_client)
    embedding_model_name = get_embedding_model_name()
    if embedding_model_name not in dimension_mapping[embedding_client]:
        logger.error(f"{embedding_model_name} does not match with any of the dimension_mapping at {embedding_client}."
                     f"Using this client you can choose: {list(dimension_mapping[embedding_client])}")
    dimension = dimension_mapping[embedding_client][embedding_model_name]

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "patterns": {"type": "text"},
                "responses": {"type": "text"},
                "document": {"type": "text"},
                "comb_qa": {"type": "text"},
                "combined_qa_vector": {"type": "dense_vector", "dims": dimension,
                                       "index": True, "similarity": "cosine"},
                "questions_vector": {"type": "dense_vector", "dims": dimension,
                                     "index": True, "similarity": "cosine"},
                "answers_vector": {"type": "dense_vector", "dims": dimension,
                                   "index": True, "similarity": "cosine"},
            }
        }
    }

    index_name = os.getenv("ELASTICSEARCH_INDEX_NAME", "cs-theory")

    host = os.getenv("ELASTICSEARCH_HOST", "localhost")
    port = os.getenv("ELASTICSEARCH_PORT", 9200)

    logger.info(f"host: {host}, port: {port}")
    es_client = ElasticSearchClient(host, port)

    force_recreate_index = os.getenv("ELASTICSEARCH_FORCE_RECREATE", "False") == "True"

    index_doc = IndexDocuments(index_settings, es_client,
                               index_name,
                               embedding_client, 
                               force_recreate_index)

    index_doc.main_indexing_workflow()


if __name__ == '__main__':
    main()
