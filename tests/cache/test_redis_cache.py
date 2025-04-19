import unittest
from unittest.mock import patch

from src.cache.base_cache import CacheException
from src.cache.redis_cache import RedisCache, RedisCacheClient


class TestRedisCache(unittest.TestCase):
    def setUp(self):
        """Set up RedisCache instance with mock Redis server."""
        self.redis_cache = RedisCache(server="redis://localhost:6379/0")

    @patch.object(RedisCacheClient, "get", return_value="cached_value")
    def test_get(self, mock_get):
        """Test retrieving a value from Redis."""
        result = self.redis_cache.get("test_key")
        self.assertEqual(result, "cached_value")
        mock_get.assert_called_with(self.redis_cache.make_and_validate_key("test_key"))

    @patch.object(RedisCacheClient, "set")
    def test_set(self, mock_set):
        """Test storing a value in Redis."""
        self.redis_cache.set("test_key", "test_value", timeout=300)
        mock_set.assert_called_with(self.redis_cache.make_and_validate_key("test_key"), "test_value", 300)

    @patch.object(RedisCacheClient, "delete", return_value=True)
    def test_delete(self, mock_delete):
        """Test deleting a key from Redis."""
        self.assertTrue(self.redis_cache.delete("test_key"))
        mock_delete.assert_called_with(self.redis_cache.make_and_validate_key("test_key"))

    @patch.object(RedisCacheClient, "get_many", return_value={"key1": "value1", "key2": "value2"})
    def test_get_many(self, mock_get_many):
        """Test retrieving multiple keys from Redis."""
        result = self.redis_cache.get_many(["key1", "key2"])
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    @patch.object(RedisCacheClient, "set_many")
    def test_set_many(self, mock_set_many):
        """Test setting multiple key-value pairs in Redis."""
        data = {"key1": "value1", "key2": "value2"}
        self.redis_cache.set_many(data, timeout=300)
        mock_set_many.assert_called_with(data, 300)

    @patch.object(RedisCacheClient, "delete_many")
    def test_delete_many(self, mock_delete_many):
        """Test deleting multiple keys from Redis."""
        keys = ["key1", "key2"]
        self.redis_cache.delete_many(keys)
        mock_delete_many.assert_called_with(keys)

    @patch.object(RedisCacheClient, "has_key", return_value=True)
    def test_has_key(self, mock_has_key):
        """Test checking if a key exists in Redis."""
        self.assertTrue(self.redis_cache.has_key("test_key"))
        mock_has_key.assert_called_with("test_key")

    @patch.object(RedisCacheClient, "touch", return_value=True)
    def test_touch(self, mock_touch):
        """Test updating key expiration time."""
        self.assertTrue(self.redis_cache.touch("test_key", timeout=600))
        mock_touch.assert_called_with(self.redis_cache.make_and_validate_key("test_key"), 600)

    @patch.object(RedisCacheClient, "incr", return_value=5)
    def test_incr(self, mock_incr):
        """Test incrementing a key's value in Redis."""
        result = self.redis_cache.incr("counter", delta=2)
        self.assertEqual(result, 5)
        mock_incr.assert_called_with(self.redis_cache.make_and_validate_key("counter"), 2)

    @patch.object(RedisCacheClient, "clear")
    def test_clear(self, mock_clear):
        """Test clearing all cache entries in Redis."""
        self.redis_cache.clear()
        mock_clear.assert_called_once()

    @patch.object(RedisCacheClient, "get_client", side_effect=CacheException("Redis connection failed"))
    def test_redis_connection_failure(self, mock_get_client):
        """Test handling Redis connection failure."""
        with self.assertRaises(CacheException):
            self.redis_cache.get("test_key")
        mock_get_client.assert_called()


if __name__ == "__main__":
    unittest.main()
