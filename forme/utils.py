import json
from typing import MutableMapping

from django.db import models
import redis



# class RedisCache(MutableMapping):
#     """
#     Redis TTL-ed wrapper for cachetools (``redis``).

#     :param cache: actual redis cache.
#     :param ttl: time-to-live in seconds, used as default expiration (``ex``), default is 600.

#     Keys and values are serialized in *JSON*.

#     .. code-block:: python

#         # redis with 1 hour expiration
#         cache = ctu.RedisCache(redis.Redis(host="localhost"), 3600)
#     """

#     def __init__(self, cache, ttl=600):
#         # import redis
#         # assert isinstance(cache, redis.Redis)
#         self._cache = cache
#         self._ttl = ttl

#     def clear(self):  # pragma: no cover
#         """Flush Redis contents."""
#         return self._cache.flushdb()

#     def _serialize(self, s):
#         return json.dumps(s, sort_keys=True)

#     def _deserialize(self, s):
#         return json.loads(s)

#     def _key(self, key):
#         return json.dumps(key, sort_keys=True)

#     def __getitem__(self, index):
#         val = self._cache.get(self._key(index))
#         if val:
#             return self._deserialize(val)
#         else:
#             raise KeyError()

#     def __setitem__(self, index, value, ttl=None):
#         if ttl is None:
#             ttl = self._ttl
#         return self._cache.set(self._key(index), self._serialize(value), ex=ttl)

#     def __delitem__(self, index):
#         return self._cache.delete(self._key(index))

#     def __len__(self):
#         return self._cache.dbsize()

#     def __iter__(self):
#         raise Exception("not implemented yet")

#     def info(self, *args, **kwargs):
#         """Return redis informations."""
#         return self._cache.info(*args, **kwargs)

#     def dbsize(self, *args, **kwargs):
#         """Return redis database size."""
#         return self._cache.dbsize(*args, **kwargs)

#     # also forward Redis set/get/delete
#     def set(self, index, value, ttl=None, **kwargs):
#         if ttl is None:
#             ttl = self._ttl
#         if "ex" not in kwargs:  # pragma: no cover
#             kwargs["ex"] = ttl
#         return self._cache.set(self._key(index), self._serialize(value), **kwargs)

#     def get(self, index, default=None):
#         """Get cache contents."""
#         return self[index]

#     def delete(self, index):
#         """Delete cache contents."""
#         del self[index]

#     # stats
#     def hits(self):
#         """Return cache hits."""
#         stats = self.info(section="stats")
#         return float(stats["keyspace_hits"]) / (
#             stats["keyspace_hits"] + stats["keyspace_misses"]
#         )

