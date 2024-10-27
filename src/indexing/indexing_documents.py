import os
import sys
import json
import logging
import logging.config
from tqdm import tqdm
from dotenv import load_dotenv

import numpy as np

if __name__ == "__main__":
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
                 embedding_client=None, 
                 force_recreate_index=os.getenv("ELASTICSEARCH_FORCE_RECREATE", 
                                                "False") == "True"
                 ) -> None:
        logger.info(f"Index documents to '{index_name}' with embedding: {embedding_client}")
        self.index_settings = index_settings
        self.index_name = index_name
        self.embedding_client = embedding_client if not None else import_embeddings("transformers")()
        self.force_recreate_index = force_recreate_index
        self.es_client = es_client

    @staticmethod
    def read_data():
        with open("data/all_qa_cleaned.json") as file:
            intents = json.load(file)
        return intents

    def get_text_embedding(self, embedding_text):
        embedding = self.embedding_client.get_embeddings([embedding_text])[0]
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        return embedding

    def get_combined_qa_embedding(self, intent):
        embedding_text_template = ("""Question: {patterns}\nAnswer:{responses}""")

        embedding_text = embedding_text_template.format(
            patterns=intent["patterns"][0],
            responses=intent["responses"][0]
        )

        embedding = self.get_text_embedding(embedding_text)

        full_text = ("""Questions:\n- {'\n- '.join(intent["patterns"])}\nAnswers:\n- {'\n- '.join(intent["responses"]}""")

        return full_text, embedding_text, embedding

    def get_questions_embedding(self, intent):

        full_text = '\n- '.join(intent["patterns"])
        embedding_text = intent["patterns"][-1]
        embedding = self.get_text_embedding(embedding_text)
        return full_text, embedding_text, embedding

    def get_answers_embedding(self, intent):
        full_text = '\n- '.join(intent["responses"])
        embedding_text = intent["responses"][-1]
        embedding = self.get_text_embedding(embedding_text)
        return full_text, embedding_text, embedding

    def get_complete_intent_for_indexing(self, intent):
        es_doc = {}
        questions_full, questions_text, questions_embedding = self.get_questions_embedding(intent)
        es_doc["questions"] = questions_full
        es_doc["questions_vector_text"] = questions_text
        es_doc["questions_vector"] = questions_embedding

        answers_full, answers_text, answers_embedding = self.get_answers_embedding(intent)
        es_doc["answers"] = answers_full
        es_doc["answers_vector_text"] = answers_text
        es_doc["answers_vector"] = answers_embedding

        comb_full, comb_text, comb_embedding = self.get_combined_qa_embedding(intent)
        es_doc["combined_qa"] = comb_full
        es_doc["combined_qa_vector_text"] = comb_text
        es_doc["combined_qa_vector"] = comb_embedding

        es_doc["id"] = intent["id"]
        es_doc["document"] = intent["document"]

        return es_doc

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

        for intent in tqdm(intents):
            intent = self.get_complete_intent_for_indexing(intent)

            self.add_document_to_index(intent)


def indexing_workflow():

    embedding_client_name = os.getenv("EMBEDDING_CLIENT", "transformer")
    check_embedding_model(embedding_client_name)
    embedding_client = import_embeddings(embedding_client_name)()
    embedding_model_name = get_embedding_model_name()
    if embedding_model_name not in embedding_client._model_dimensions:
        logger.error(f"{embedding_model_name} does not match with any of the dimension_mapping at {embedding_client_name}."
                     f"Using this client you can choose: {list(embedding_client._model_dimensions)}")
        return None
    dimension = embedding_client._model_dimensions[embedding_model_name]

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "document": {"type": "text"},
                "questions": {"type": "text"},
                "answers": {"type": "text"},
                "combined_qa": {"type": "text"},
                "questions_vector_text": {"type": "text"},
                "answers_vector_text": {"type": "text"},
                "combined_qa_vector_text": {"type": "text"},
                "combined_qa_vector": {"type": "dense_vector", "dims": dimension},
                "questions_vector": {"type": "dense_vector", "dims": dimension},
                "answers_vector": {"type": "dense_vector", "dims": dimension},
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
    indexing_workflow()
