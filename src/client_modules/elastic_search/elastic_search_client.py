import os
import logging
from typing import List

from elasticsearch import Elasticsearch
from tqdm.auto import tqdm


logger = logging.getLogger(__name__)

class ElasticSearchClient:

    """
    Run Elastic Search in docker running in the terminal:

    docker run -it \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -v elasticsearch_data:/usr/share/elasticsearch/data \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3

    and check it with:

    curl http://localhost:9200
    """

    def __init__(self, host=os.getenv("ELASTICSEARCH_HOST", "localhost"),
                 port=os.getenv("ELASTICSEARCH_PORT", 9200)):
        
        url = f"http://{host}:{port}"
        logger.info(f"Starting ElasticSearch {url}")
        self.client = Elasticsearch(url)

        logger.info(self.client.info())

    def create_index(self, index_name, index_settings):
        logger.info(self.client.info())
        self.client.indices.delete(index=index_name, ignore_unavailable=True)
        response = self.client.indices.create(index=index_name, body=index_settings)
        return response
    
    def index_documents(self, index_name, documents: List[dict]):
        for doc in tqdm(documents):
            self.client.index(index=index_name, document=doc)

    def search(self, index_name, search_query):
        """
        Query DSL info: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html#query-dsl

        Example of query: here, the question match are consider above the rest.

        search_query = {
            "size": max_results,
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": ["question^3", "text", "section"],
                            "type": "best_fields"
                        }
                    },
                    "filter": {
                        "term": {
                            "course": "data-engineering-zoomcamp"
                        }
                    }
                }
            }
        }
        """
        return self.client.search(index=index_name, body=search_query)
    
    def extract_info_from_search(self, response):
        documents = [hit['_source'] for hit in response['hits']['hits']]
        return documents
    
    def index_exists(self, index_name):
        if self.client.indices.exists(index=index_name):
            logger.info(f"The index '{index_name}' already exists.")
            return True
        else:
            logger.info(f"The index '{index_name}' does not exists.")
            return False

    def delete_index(self, index_name):
        self.client.indices.delete(index=index_name, ignore_unavailable=True)
        logger.info(f"Deleted index '{index_name}'")
