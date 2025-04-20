# 🚀 CacheMaster - High-Performance Caching Library

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![MIT License](https://img.shields.io/badge/license-MIT-green)
[![PyPI version](https://img.shields.io/pypi/v/cachemaster)](https://pypi.org/project/cachemaster/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/JanardhanSingh98/CacheMaster/pypi-publish.yml?branch=main)](https://github.com/JanardhanSingh98/CacheMaster/actions/workflows/pypi-publish.yml)

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
│── CHANGELOG.md
│── poetry.lock
│── pyproject.toml
│── README.md
│── LICENSE
│── .bumpver.toml
│── .gitignore
```

## 📦 Installation
CacheMaster requires Python 3.7+ and the following dependencies:

### **🔧 Dependencies:**
- `redis>=4.0.0`  – Required for Redis-based caching
- `pytest>=7.0.0` – For testing
- `pytest-mock>=3.10` – Mocks for testing
- `poetry>=2.1.2` – For packaging

### **📥 Installation**

```sh
pip install CacheMaster
```
Or using Poetry:

```sh
poetry add dict2objects
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

## 🛠 Development & Contribution

1. Clone the repository:
   ```sh
   git clone git@github.com:JanardhanSingh98/CacheMaster.git
   cd CacheMaster
   ```
2. Install dependencies:
   ```sh
   poetry install
   ```
3. Run tests:
   ```sh
   poetry run coverage run --omit="tests*" -m pytest
   ```

---

## 🎯 How CacheMaster Helps You
- 🚀 **Boosts performance** by reducing redundant database queries.
- 💾 **Efficient memory management** with TTL-based expiration.
- 🔄 **Scalable & flexible** with both local and distributed caching.
- 📌 **Easy to integrate** with existing applications.

## 🐜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### 🌟 **Like this project? Give it a star ⭐ on GitHub!**

