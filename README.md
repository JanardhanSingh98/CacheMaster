# 🚀 CacheMaster - High-Performance Caching Library

CacheMaster is a high-performance caching library that supports both **in-memory** and **Redis-based caching**. It provides a simple, flexible API for efficiently storing, retrieving, and managing cache data.

## ✨ Features
- ✅ **Supports In-Memory & Redis Caching**
- 🔒 **Thread-safe** local caching
- 🛠 **Customizable serialization** (Pickle & JSON for Redis)
- ⏳ **Automatic expiration & TTL management**
- ⚡ **Batch operations for performance optimization**
- 🎯 **Decorator support for function caching**

## 📂 Project Structure
```
CacheMaster/
│── src/
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── base_cache.py
│   │   ├── core_cache.py
│   │   ├── mem_cache.py
│   │   ├── redis_cache.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── cache_config.py
│── tests/
│── pyproject.toml
│── setup.cfg
│── setup.py
│── README.md
│── LICENSE
│── .gitignore
```

## 📦 Installation
```sh
pip install cachemaster
```

## 🚀 Running the Cache Application
To start using CacheMaster, initialize a cache instance:
```python
from cachemaster.core_cache import CoreCache, CacheType

# Local (In-Memory) Cache
local_cache = CoreCache(app_name="my_app", cache_type=CacheType.LOCAL_CACHE)

# Redis Cache
redis_cache = CoreCache(app_name="my_app", cache_type=CacheType.REDIS_CACHE, redis_url="redis://localhost")
```

## 🔥 Usage
### Basic Cache Operations
```python
# Set and Get
local_cache.set("user_123", {"name": "John"}, timeout=600)
user = local_cache.get("user_123")  # Returns: {"name": "John"}

# Delete
local_cache.delete("user_123")

# Check if key exists
exists = local_cache.has_key("user_123")  # Returns: False
```

### Function Caching with Decorators
```python
@redis_cache.decorator_cache(namespace="users", timeout=300, keys=["user_id"])
def get_user_data(user_id):
    return expensive_database_call(user_id)
```

### Batch Operations
```python
# Set multiple values
local_cache.set_many({"key1": "value1", "key2": "value2"}, timeout=300)

# Get multiple values
values = local_cache.get_many(["key1", "key2"])  # Returns: {"key1": "value1", "key2": "value2"}

# Delete multiple values
local_cache.delete_many(["key1", "key2"]) 
```

### Incrementing & Decrementing
```python
local_cache.set("counter", 10)
local_cache.incr("counter", 2)  # 12
local_cache.decr("counter", 1)  # 11
```

## 🛠 Running Tests
To ensure everything works correctly, run:
```sh
pytest tests/
```

## 🎯 How CacheMaster Helps You
- 🚀 **Boosts performance** by reducing redundant database queries.
- 💾 **Efficient memory management** with TTL-based expiration.
- 🔄 **Scalable & flexible** with both local and distributed caching.
- 📌 **Easy to integrate** with existing applications.

## 📜 License
MIT License

