import time
import unittest

from src.cache.base_cache import BaseCache, CacheException


class TestBaseCache(unittest.TestCase):

    def setUp(self):
        self.cache = BaseCache()

    def test_add_and_get(self):
        self.cache.add("key1", "value1", timeout=5)
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.cache.get("nonexistent_key"))

    def test_set_and_get(self):
        self.cache.set("key2", "value2", timeout=5)
        self.assertEqual(self.cache.get("key2"), "value2")

    def test_expiration(self):
        self.cache.set("key3", "value3", timeout=1)
        time.sleep(2)
        self.assertIsNone(self.cache.get("key3"))

    def test_incr_and_decr(self):
        self.cache.set("key4", 1, timeout=5)
        self.assertEqual(self.cache.incr("key4", 2), 3)
        self.assertEqual(self.cache.decr("key4", 1), 2)

    def test_incr_non_numeric(self):
        self.cache.set("key5", "value5", timeout=5)
        with self.assertRaises(CacheException):
            self.cache.incr("key5", 1)

    def test_delete(self):
        self.cache.set("key6", "value6", timeout=5)
        self.assertTrue(self.cache.delete("key6"))
        self.assertIsNone(self.cache.get("key6"))

    def test_clear(self):
        self.cache.set("key7", "value7", timeout=5)
        self.cache.clear()
        self.assertIsNone(self.cache.get("key7"))

    def test_touch(self):
        self.cache.set("key8", "value8", timeout=1)
        self.cache.touch("key8", timeout=5)
        time.sleep(2)
        self.assertEqual(self.cache.get("key8"), "value8")


if __name__ == "__main__":
    unittest.main()
