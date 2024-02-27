import os
from hashlib import blake2b

import diskcache as dc

cache = dc.Cache(
    # 100 MB cache size
    size_limit=int(os.getenv("CACHE_SIZE_LIMIT", 100 * 1024 * 1024)),
)


def get_cache_key(*args, **kwargs):
    hasher = blake2b(digest_size=16)
    hasher.update(str(args).encode())
    hasher.update(str(kwargs).encode())
    return hasher.hexdigest()


def get_from_cache(key):
    return cache.get(key)


def set_to_cache(key, value):
    cache.set(key, value)
