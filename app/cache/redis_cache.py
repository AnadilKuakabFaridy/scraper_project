import redis

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def get(self, key):
        value = self.redis.get(key)
        return float(value) if value else None

    def set(self, key, value):
        self.redis.set(key, value)

    def clear(self):
        self.redis.flushdb()