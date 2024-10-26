import os

import numpy as np

from src.client_modules.elastic_search.elastic_search_client import ElasticSearchClient
from src.client_modules.utils import import_embeddings


class Retrieval:

    def __init__(self,
                 es_client=ElasticSearchClient(),
                 index_name=os.getenv("ELASTICSEARCH_INDEX_NAME", "cs-theory"),
                 embedding_client=None) -> None:

        self.es_client = es_client
        self.index_name = index_name
        self.embedding_client = embedding_client if not None else import_embeddings("transformers")()

    def calc_embedding_from_text(self, text):
        embedding = self.embedding_client.get_embeddings([text])[0]
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        return embedding

    def search_with_cosine_from_embedding(self, embedding):
        search_query = {
            "query": {
                "script_score": {
                    "query": { "match_all": {} },
                    "script": {
                        "source": """
                        0.5 * dotProduct(params.query_vector, 'combined_qa_vector') +
                        0.25 * dotProduct(params.query_vector, 'answers_vector') +
                        0.25 * dotProduct(params.query_vector, 'questions_vector')
                        """,
                        "params": {
                            "query_vector": embedding
                        }
                    }
                }
            },
            "_source": ["id", "document", "questions", "questions_vector_text", "answers", "answers_vector_text", 
                        "combined_qa", "combined_qa_vector_text"]
        }

        res = self.es_client.search(index_name=self.index_name, search_query=search_query)
        return res["hits"]["hits"]

    def search_from_text(self, text):
        embedding = self.calc_embedding_from_text(text)
        results = self.search_with_cosine_from_embedding(embedding)
        return results
