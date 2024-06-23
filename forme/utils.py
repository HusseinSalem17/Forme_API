import json
from typing import MutableMapping

from django.db import models
import redis
import os

from rest_framework import status
from rest_framework.response import Response
from urllib.parse import quote


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

def get_file_path(folder, type, filename):
    # Create the folder path with the name
    folder_path = f"{folder}/{type}/"
    # Return the full file path
    print('folder_path', folder_path)
    return os.path.join(folder_path, filename)


from rest_framework.exceptions import ErrorDetail

def flatten_errors(errors):
    flattened_errors = []

    # Check if errors is a list of ErrorDetail objects or a single string
    if isinstance(errors, list) and all(isinstance(error, ErrorDetail) for error in errors):
        return " ".join(str(error) for error in errors)
    elif isinstance(errors, str):  # Directly return the string if errors is a string
        return errors

    non_field_errors = errors.pop("non_field_errors", None)
    for field, messages in errors.items():
        if isinstance(messages, dict):  # Check if the error is nested
            errors = {**errors, **messages}
            errors.pop(field)
            for key, value in messages.items():
                # Ensure messages are treated as lists before joining
                if isinstance(value, list):
                    flattened_errors.append(" ".join(str(message) for message in value))
                else:
                    flattened_errors.append(str(value))
        else:
            # Ensure messages are treated as lists before joining
            if isinstance(messages, list):
                flattened_errors.append(" ".join(str(message) for message in messages))
            else:
                flattened_errors.append(str(messages))
    if non_field_errors is not None:
        # Ensure non_field_errors are treated as lists before extending
        if isinstance(non_field_errors, list):
            flattened_errors.extend(non_field_errors)
        else:
            flattened_errors.append(str(non_field_errors))
    return " ".join(flattened_errors)


def handle_validation_error(e):
    errors = e.detail
    print("errors here", errors)
    flattened_errors = flatten_errors(errors)
    print("here flattened_errors", flattened_errors)
    return Response({"error": flattened_errors}, status=status.HTTP_400_BAD_REQUEST)

def sanitize_path_component(path_component):
    safe_component = quote(path_component, safe="")
    return "".join(
        [c if c.isalnum() or c in (" ", "-", "_") else "_" for c in safe_component]
    )