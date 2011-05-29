#! /usr/bin/env python
# Encoding: UTF-8

from regeneration.battle.moveeffect import MoveEffect

from regeneration.pokey import effects
from regeneration.pokey.registry import Registry

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class MoveRegistry(Registry):
    def get_key(self, kind):
        return kind.effect_id

move_effect_registry = registry = MoveRegistry()

@registry.put(1)
class Tackle(MoveEffect):
    pass

@registry.put(37)
class TriAttack(MoveEffect):
    def do_secondary_effect(self, hit):
        if not hit.target.fainted:
            effect_class = self.field.random_choice([
                    effects.Paralysis,
                    effects.Burn,
                    effects.Freeze,
                ], "Choose the Tri Attack effect")
            effect = self.user.give_effect(hit.target, effect_class())
            if effect:
                self.field.message(effect.messages.Applied,
                        battler=effect.subject)
