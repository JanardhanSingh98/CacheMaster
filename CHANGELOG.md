# 📦 Changelog

All notable changes to this project will be documented in this file.

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) principles and adheres to [Semantic Versioning](https://semver.org/).


## [0.1.0] - 2024-04-20

### Added
- Core caching logic for in-memory and Redis backend support
- `BaseCache` interface and concrete implementations (`MemCache`, `RedisCache`)
- Batch operations for set, get, delete
- TTL and auto-expiry handling
- Decorator-based function caching
- Version-aware cache keys
- Initial unit tests for core, Redis, and memory cache
- Async support for Redis caching using `aioredis`
- Auto-refresh mechanism for expired cache keys via `refresh_callback`
- GitHub Actions workflow to bump version and tag release automatically
- Ruff integration for linting, unused import removal, and import sorting
- `.bumpver.toml` for consistent semantic versioning
- CI integration for formatting (black), linting (ruff), typing (mypy), and testing (pytest)


### Changed
- Logging integrated across Redis cache client methods for better observability
- Migrated `pyproject.toml` to modern PEP 621-compliant configuration
- Removed `flake8`, `isort`, and `autoflake` in favor of `ruff`

