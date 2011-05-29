#! /usr/bin/env python
# Encoding: UTF-8

import functools
import weakref

# For an example, we can use veekun's pokedex database.
from pokedex.db import tables, connect

__copyright__ = 'Copyright 2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class Loader(object):
    _identifier_cache = weakref.WeakValueDictionary()

    def __init__(self, session, generation):
        self.session = session
        self.generation = generation
        if self.generation != 5:
            raise ValueError('Only Generation V is implemented')

        self.natures = session.query(tables.Nature).all()

        self.battle_stats = session.query(tables.Stat).order_by(
                tables.Stat.id).all()

        self.permanent_stats = [s for s in self.battle_stats if
                not s.is_battle_only]

    def _cached(func):
        @functools.wraps(func)
        def cached(self, *args):
            key = self.session, func, args
            try:
                return self._identifier_cache[key]
            except KeyError:
                result = func(self, *args)
                self._identifier_cache[key] = result
                return result
        return cached

    @_cached
    def load_form(self, identifier, form_identifier=None):
        query = self.session.query(tables.PokemonForm)
        query = query.join(tables.PokemonForm.pokemon)
        query = query.join(tables.Pokemon.species)
        query = query.filter(tables.PokemonForm.form_identifier ==
                form_identifier)
        query = query.filter(tables.PokemonSpecies.identifier == identifier)
        return query.one()

    @_cached
    def load_by_identifier(self, table, identifier):
        query = self.session.query(table)
        query = query.filter(table.identifier == identifier)
        return query.one()

    def _loader(table):
        def load(self, identifier):
            return self.load_by_identifier(table, identifier)
        return load

    load_move = _loader(tables.Move)
    load_nature = _loader(tables.Nature)
    load_ability = _loader(tables.Ability)
    load_item = _loader(tables.Item)
    load_stat = _loader(tables.Stat)

    def load_struggle(self):
        return self.load_move('struggle')

    def load_types(self, identifiers):
        results = []
        for name in names:
            return self.load_type(identifiers)

default_loader = Loader(connect(), 5)
