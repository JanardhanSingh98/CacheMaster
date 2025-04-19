import logging
import threading

from src.cache.base_cache import CacheException
from src.cache.core_cache import CacheType, CoreCache

logger = logging.getLogger(__name__)


class SingletonCache:
    """Thread-safe Singleton class for managing a single instance of CoreCache."""

    _instance: "SingletonCache" = None
    _cache: CoreCache | None = None
    _lock = threading.Lock()

    def __init__(self):
        raise CacheException("Use `get_instance()` instead of instantiating directly.")

    @classmethod
    def get_instance(
        cls, app_name: str, cache_type: CacheType | str = CacheType.REDIS_CACHE, *args, **kwargs
    ) -> CoreCache:
        """
        Returns a singleton instance of CoreCache.

        Args:
            app_name (str): The application name.
            cache_type (CacheType | str): The type of cache (e.g., Redis or Local).
            *args: Additional positional arguments for CoreCache.
            **kwargs: Additional keyword arguments for CoreCache.

        Returns:
            CoreCache: The singleton CoreCache instance.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logger.debug("Initializing CoreCache singleton instance.")
                    cls._instance = cls.__new__(cls)
                    cls._cache = CoreCache(app_name=app_name, cache_type=cache_type, *args, **kwargs)
        return cls._cache

    @classmethod
    def initialize_cache(cls, app_name: str, cache_type: CacheType | str = CacheType.REDIS_CACHE):
        """
        Initializes the cache connection.

        Args:
            app_name (str): The application name.
            cache_type (CacheType | str): The type of cache to initialize.
        """
        logger.debug("Initializing cache connection.")
        cls.get_instance(app_name, cache_type)
        if cls._cache.cache_type == CacheType.REDIS_CACHE:
            cls._cache.redis_cache.start()

    @classmethod
    def close_cache(cls):
        """
        Closes the cache connection and resets the singleton instance.
        """
        if cls._instance:
            logger.debug("Closing cache connection.")
            if cls._cache.cache_type == CacheType.REDIS_CACHE:
                cls._cache.redis_cache.close()
            cls._instance = None
            cls._cache = None

    @classmethod
    def get_redis_client(cls, app_name: str):
        """
        Returns the Redis client instance.

        Args:
            app_name (str): The application name.

        Returns:
            Redis: The Redis client instance.

        Raises:
            CacheException: If Redis cache is not initialized.
        """
        if cls._instance is None:
            cls.get_instance(app_name, CacheType.REDIS_CACHE)

        if not cls._cache or not cls._cache.redis_cache:
            raise CacheException("Redis cache is not initialized.")

        return cls._cache.redis_cache.client
