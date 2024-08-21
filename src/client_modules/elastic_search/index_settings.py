class ElasticSearchIndexSettings:

    def __init__(self, name, index_settings=None, n_shards=1, n_replicas=0, properties=None):
        """
        Simple base of an Index Settings
        
        properties need to be in the format: 
        {
            "var_name": {"type": type},
            .
            .
        }
        type can be text,... or keyword, that means it will filter with it.

        Example of settings:

        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "section": {"type": "text"},
                    "question": {"type": "text"},
                    "course": {"type": "keyword"} 
                }
            }
        }
        """
        
        self.name = name
        if index_settings:
            self._n_shards = index_settings['settings'].get("number_of_shards", None)
            self._n_replicas = index_settings['settings'].get("number_of_replicas", None)
            self._properties = index_settings['settings'].get("properties", None)
        else:
            self._n_shards = n_shards
            self._n_replicas = n_replicas
            self._properties = properties

        self.index_settings = index_settings if index_settings else self.build_index_settings()
        

    def _build_settings(self):
        return {
            "number_of_shards": self.n_shards,
            "number_of_replicas": self.n_replicas
        }

    def _build_mapping(self):
        return {
            "properties": self.properties
        }
    
    def build_index_settings(self):
        return {
            "settings": self._set_settings(),
            "mapping": self._mapping()
        }