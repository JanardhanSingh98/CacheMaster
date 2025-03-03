import threading

from src.cache.base_cache import CacheException
from src.cache.core_cache import CoreCache, CacheType


class SingletonCache:
    """Thread-safe Singleton class for managing a single instance of CoreCache."""

    _instance = None
    _cache = None
    _lock = threading.Lock()  # Ensuring thread safety

    def __init__(self):
        raise CacheException("Call `instance()` instead of instantiating directly.")

    @classmethod
    def instance(cls, app_name: str, cache_type: str | CacheType = CacheType.REDIS_CACHE, *args, **kwargs) -> CoreCache:
        """Returns a singleton instance of the CoreCache."""
        if cls._instance is None:
            with cls._lock:  # Prevents race conditions
                if cls._instance is None:  # Double-check locking
                    cls._instance = cls.__new__(cls)
                    cls._cache = CoreCache(app_name=app_name, cache_type=cache_type, *args, **kwargs)
        return cls._cache

    @classmethod
    def start_connection(cls, app_name: str, cache_type: CacheType = CacheType.REDIS_CACHE):
        """Starts the cache connection, allowing different cache types."""
        cls.instance(app_name, cache_type)
        if cls._cache.cache_type == CacheType.REDIS_CACHE:
            cls._cache.redis_cache.start()

    @classmethod
    def close_connection(cls):
        """Closes the cache connection and resets the singleton instance."""
        if cls._instance:
            if cls._cache.cache_type == CacheType.REDIS_CACHE:
                cls._cache.redis_cache.close()
            cls._instance = None
            cls._cache = None

    @classmethod
    def redis_client(cls, app_name: str):
        """Returns the Redis client instance, ensuring Redis cache is initialized."""
        if cls._instance is None:
            cls.instance(app_name, CacheType.REDIS_CACHE)

        if cls._cache is None or cls._cache.redis_cache is None:
            raise CacheException("Redis cache has not been initialized.")

        return cls._cache.redis_cache.client
