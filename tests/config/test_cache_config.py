import unittest
from unittest.mock import MagicMock, patch

from src.cache.base_cache import CacheException
from src.cache.core_cache import CacheType
from src.config.cache_config import SingletonCache


class TestSingletonCache(unittest.TestCase):

    @patch("src.config.cache_config.CoreCache")
    def test_get_instance_creates_singleton(self, MockCoreCache):
        instance1 = SingletonCache.get_instance("test_app", CacheType.LOCAL_CACHE)
        instance2 = SingletonCache.get_instance("test_app", CacheType.LOCAL_CACHE)
        self.assertIs(instance1, instance2)
        MockCoreCache.assert_called_once_with(app_name="test_app", cache_type=CacheType.LOCAL_CACHE)

    @patch("src.config.cache_config.CoreCache")
    def test_initialize_cache(self, MockCoreCache):
        mock_cache = MockCoreCache.return_value
        mock_cache.cache_type = CacheType.REDIS_CACHE
        mock_cache.redis_cache = MagicMock()

        SingletonCache.initialize_cache("test_app", CacheType.REDIS_CACHE)
        mock_cache.redis_cache.start.assert_called_once()

    @patch("src.config.cache_config.CoreCache")
    def test_close_cache(self, MockCoreCache):
        mock_cache = MockCoreCache.return_value
        mock_cache.cache_type = CacheType.REDIS_CACHE
        mock_cache.redis_cache = MagicMock()

        SingletonCache.initialize_cache("test_app", CacheType.REDIS_CACHE)
        SingletonCache.close_cache()
        mock_cache.redis_cache.close.assert_called_once()
        self.assertIsNone(SingletonCache._instance)
        self.assertIsNone(SingletonCache._cache)

    @patch("src.config.cache_config.CoreCache")
    def test_get_redis_client(self, MockCoreCache):
        mock_cache = MockCoreCache.return_value
        mock_cache.redis_cache = MagicMock()
        mock_cache.redis_cache.client = "mock_redis_client"

        client = SingletonCache.get_redis_client("test_app")
        self.assertEqual(client, "mock_redis_client")

    def test_get_redis_client_raises_exception_if_not_initialized(self):
        with self.assertRaises(CacheException) as context:
            SingletonCache.get_redis_client("test_app")
        self.assertEqual(str(context.exception), "Redis cache is not initialized.")

    def test_direct_instantiation_raises_exception(self):
        with self.assertRaises(CacheException) as context:
            SingletonCache()
        self.assertEqual(str(context.exception), "Use `get_instance()` instead of instantiating directly.")


if __name__ == "__main__":
    unittest.main()
