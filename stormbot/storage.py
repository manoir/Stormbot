import os
import json
import collections.abc

class ProxyEncoder(json.JSONEncoder):
    def default(self, o):
        return o._cache

class ListProxy(collections.abc.MutableSequence):
    def __init__(self, storage, cache=None):
        self._storage = storage
        self._cache = cache or []

    def __getitem__(self, index):
        return self._storage.proxy(self._cache.__getitem__(index))

    def __setitem__(self, index, value):
        self._cache.__setitem__(index, self._storage.proxy(value))
        self._storage.dump()

    def __delitem__(self, index):
        self._cache.__delitem__(index)
        self._storage.dump()

    def insert(self, index, value):
        ret = self._cache.insert(index, value)
        self._storage.dump()
        return ret

    def __len__(self):
        return self._cache.__len__()

class DictProxy(collections.abc.MutableMapping):
    def __init__(self, storage, cache=None):
        self._storage = storage
        self._cache = cache or {}

    def __getitem__(self, key):
        return self._storage.proxy(self._cache.__getitem__(key))

    def __setitem__(self, key, value):
        self._cache.__setitem__(key, self._storage.proxy(value))
        self._storage.dump()

    def __delitem__(self, key):
        self._cache.__delitem__(key)
        self._storage.dump()

    def __iter__(self):
        return self._cache.__iter__()

    def __len__(self):
        return self._cache.__len__()

class Storage(DictProxy):
    def __init__(self, path):
        super().__init__(self)
        self.path = path
        if os.path.isfile(self.path):
            with open(self.path, 'r') as cachefile:
                self._cache = json.load(cachefile)

    def proxy(self, value):
        if isinstance(value, list):
            return ListProxy(self, value)
        if isinstance(value, dict):
            return DictProxy(self, value)
        return value

    def dump(self):
        with open(self.path, 'w') as cachefile:
            json.dump(self._cache, cachefile, cls=ProxyEncoder)
