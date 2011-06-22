#! /usr/bin/env python
# Encoding: UTF-8

import re

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class Registry(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.registry = dict()

    def get_key(self, key):
        return key

    def insert_key(self, key):
        return key

    def get(self, key):
        try:
            return self.registry[self.get_key(key)]
        except KeyError:
            try:
                parent_get = self.parent.get
            except AttributeError:
                raise KeyError(key)
            else:
                return parent_get(key)

    def __setitem__(self, key, item):
        key = self.insert_key(key)
        assert key not in self.registry
        self.registry[key] = item

    def __getitem__(self, key):
        return self.get(key)

    def put(self, key):
        def putter(cls):
            self[key] = cls
            return cls
        return putter

class EntityRegistry(Registry):
    def get_key(self, entity):
        return entity.identifier

    def insert_key(self, identifier):
        return re.sub('([A-Z])', r'-\1', identifier).lstrip('-').lower()

    def register(self, cls):
        self[cls.__name__] = cls
        return cls
