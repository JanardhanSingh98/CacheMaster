import asyncio
import logging
import unittest
from unittest.mock import patch

from src.cache.core_cache import CacheException, CacheType, CoreCache

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class TestCoreCache(unittest.TestCase):

    @patch("src.cache.mem_cache.LocMemCache")
    def test_local_cache_initialization(self, MockLocMemCache):
        cache = CoreCache(app_name="test_app", cache_type=CacheType.LOCAL_CACHE)
        self.assertIsInstance(cache.local_cache, MockLocMemCache)
        self.assertIsNone(cache.redis_cache)

    @patch("src.cache.redis_cache.RedisCacheClient")
    def test_redis_cache_initialization(self, MockRedisCacheClient):
        cache = CoreCache(app_name="test_app", cache_type=CacheType.REDIS_CACHE, redis_url="redis://localhost:6379/0")
        self.assertIsInstance(cache.redis_cache, MockRedisCacheClient)
        self.assertIsNone(cache.local_cache)

    def test_redis_cache_initialization_without_url(self):
        with self.assertRaises(CacheException) as context:
            CoreCache(app_name="test_app", cache_type=CacheType.REDIS_CACHE)
        self.assertEqual(str(context.exception), "Redis URL is missing. Pass `redis_url` in kwargs.")

    @patch("src.cache.mem_cache.LocMemCache")
    def test_decorator_cache_sync_function(self, MockLocMemCache):
        cache = CoreCache(app_name="test_app", cache_type=CacheType.LOCAL_CACHE)
        MockLocMemCache().get.return_value = None

        @cache.decorator_cache(namespace="test_namespace", timeout=60)
        def test_func(x, y):
            return x + y

        result = test_func(1, 2)
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
        self.assertEqual(result, 3)
        MockLocMemCache().set.assert_called_once()

    @patch("src.cache.mem_cache.LocMemCache")
    async def test_decorator_cache_async_function(self, MockLocMemCache):
        cache = CoreCache(app_name="test_app", cache_type=CacheType.LOCAL_CACHE)
        MockLocMemCache().get.return_value = None

        @cache.decorator_cache(namespace="test_namespace", timeout=60)
        async def test_func(x, y):
            return x + y

        result = await test_func(1, 2)
        self.assertEqual(result, 3)
        MockLocMemCache().set.assert_called_once()


if __name__ == "__main__":
    unittest.main()
