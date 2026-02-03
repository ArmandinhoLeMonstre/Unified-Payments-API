import redis
import json

class RedisCache:
    def __init__(self, client):
        self.client = client
    
    def set_cache(self, key, value):
        # if key or value is None:
        #     return (0)

        self.client.set(key, value)
    
    def get_cache(self, key):
        if key is None:
            return (0)

        cache = self.client.get(key)
        
        return(cache)
    
    def clear_all_keys(self):
        self.client.flushdb()