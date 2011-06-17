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

class UserStatBoostMove(MoveEffect):
    def use(self, **kwargs):
        raised_stat = self.field.loader.load_stat(self.stat_identifier)
        self.user.raise_stat(raised_stat, self.delta, verbose=True)

class ConversionMove(MoveEffect):
    def convert(self, possible_types):
        possible_types = list(t for t in possible_types if
                t not in self.user.types)
        if possible_types:
            new_type = self.field.random_choice(possible_types,
                    "Select type to convert to")
            self.user.types = [new_type]
            self.field.message(messages.ConvertedType, battler=self.user,
                    new_type=new_type, moveeffect=self)
        else:
            self.fail()

@registry.put(1)
class Tackle(MoveEffect):
    pass

@registry.put(11)
class Sharpen(UserStatBoostMove):
    stat_identifier = 'attack'
    delta = +1

@registry.put(31)
class Conversion(ConversionMove):
    def use(self):
        self.convert(m.type for m in self.user.moves)

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

@registry.put(53)
class Agility(UserStatBoostMove):
    stat_identifier = 'speed'
    delta = +2

@registry.put(94)
class Conversion2(ConversionMove):
    def hit(self, hit):
        try:
            last_type = hit.target.used_move_effects[-1].type
        except IndexError:
            self.fail()
        else:
            if last_type:
                self.convert(e.target_type for e in last_type.damage_efficacies
                        if e.damage_factor < 100)
            else:
                self.fail()

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
