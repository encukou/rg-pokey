#! /usr/bin/env python
# Encoding: UTF-8

from regeneration.battle.moveeffect import MoveEffect

from regeneration.pokey import effects
from regeneration.pokey import messages
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

@registry.put(11)
class Sharpen(MoveEffect):
    def use(self, **kwargs):
        raised_stat = self.field.loader.load_stat('attack')
        self.user.raise_stat(raised_stat, +1, verbose=True)

@registry.put(31)
class Conversion(MoveEffect):
    def use(self, **kwargs):
        eligible_types = []
        for move in self.user.moves:
            if move.type not in self.user.types:
                eligible_types.append(move.type)
        if eligible_types:
            new_type = self.field.random_choice(eligible_types,
                    "Select type to convert to")
            self.user.types = [new_type]
            self.field.message(messages.ConvertedType, battler=self.user,
                    new_type=new_type, moveeffect=self)
        else:
            self.fail()

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

@registry.put(255)
class Struggle(MoveEffect):
    def __init__(self, *args, **kwargs):
        super(Struggle, self).__init__(*args, **kwargs)
        self.type = None

    def hit(self, hit):
        super(Struggle, self).hit(hit)
        self.user.do_damage(self.user.stats.hp // 4,
                message_class=messages.Recoil)

@registry.put(260)
class TrickRoom(MoveEffect):
    def use(self, **kwargs):
        existing_effect = self.field.get_effect(effects.TwistedDimensions)
        if existing_effect:
            existing_effect.remove()
            self.field.message(messages.NormalDimensions)
        else:
            self.user.give_effect(self.field, effects.TwistedDimensions())
            self.field.message(messages.TwistedDimensions, battler=self.user)
