#! /usr/bin/env python
# Encoding: UTF-8

import functools

from regeneration.battle.move import Move as BaseMove

from regeneration.pokey.moveeffects import move_effect_registry

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class Move(BaseMove):
    def __init__(self, kind, maxpp=None, generation=None):
        if not generation:
            raise ValueError('Move needs a generation')
        self.generation = generation
        super(Move, self).__init__(kind, maxpp)

    def get_targetting(self, identifier):
        identifier = identifier.replace('other-pokemon', 'others')
        identifier = identifier.replace('pokemon', 'battler')
        return super(Move, self).get_targetting(identifier)

    def get_effect(self, user, target):
        cls = move_effect_registry[self.kind]
        return cls(self, user, target)
