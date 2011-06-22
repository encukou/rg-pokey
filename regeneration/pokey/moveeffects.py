#! /usr/bin/env python
# Encoding: UTF-8

from __future__ import division

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

class UserStatChangeMove(MoveEffect):
    def use(self, **kwargs):
        stat = self.field.loader.load_stat(self.stat_identifier)
        self.user.change_stat(stat, self.delta, verbose=True)

class TargetStatChangeMove(MoveEffect):
    def hit(self, hit):
        stat = self.field.loader.load_stat(self.stat_identifier)
        hit.target.change_stat(stat, self.delta, verbose=True)

class TargetSecondaryStatChangeMove(MoveEffect):
    def do_secondary_effect(self, hit):
        if not hit.target.fainted:
            stat = self.field.loader.load_stat(self.stat_identifier)
            hit.target.change_stat(stat, self.delta, verbose=True)

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

class SecondaryStatusMove(MoveEffect):
    def do_secondary_effect(self, hit):
        if not hit.target.fainted:
            effect_class = self.effect_class
            self.user.give_effect(hit.target, effect_class(),
                    message_class=effect_class.messages.Applied,
                    battler=hit.target)

@registry.put(1)
class Tackle(MoveEffect):
    pass

@registry.put(5)
class Flamethrower(SecondaryStatusMove):
    effect_class = effects.Burn

@registry.put(6)
class IceBeam(SecondaryStatusMove):
    effect_class = effects.Freeze

@registry.put(7)
class Thunderbolt(SecondaryStatusMove):
    effect_class = effects.Paralysis

@registry.put(11)
class Sharpen(UserStatChangeMove):
    stat_identifier = 'attack'
    delta = +1

@registry.put(12)
class Sharpen(UserStatChangeMove):
    stat_identifier = 'defense'
    delta = +1

@registry.put(17)
class DoubleTeam(UserStatChangeMove):
    stat_identifier = 'evasion'
    delta = +1

@registry.put(19)
class Growl(TargetStatChangeMove):
    stat_identifier = 'attack'
    delta = -1

@registry.put(20)
class TailWhip(TargetStatChangeMove):
    stat_identifier = 'defense'
    delta = -1

@registry.put(21)
def effect21(move, user, target):
    """Move effect #21 factory

    StringShot and Electroweb/Low Sweep share the same effect code, but
    otherwise are entirely different.
    """
    if move.power:
        return Electroweb(move, user, target)
    else:
        return StringShot(move, user, target)

class StringShot(TargetStatChangeMove):
    stat_identifier = 'speed'
    delta = -1

class Electroweb(TargetSecondaryStatChangeMove):
    stat_identifier = 'speed'
    delta = -1

    def __init__(self, *args, **kwargs):
        super(Electroweb, self).__init__(*args, **kwargs)
        self.effect_chance = 100

@registry.put(24)
class Flash(TargetStatChangeMove):
    stat_identifier = 'accuracy'
    delta = -1

@registry.put(25)
class SweetScent(TargetStatChangeMove):
    stat_identifier = 'evasion'
    delta = -1

@registry.put(31)
class Conversion(ConversionMove):
    def use(self):
        self.convert(m.type for m in self.user.moves)

@registry.put(33)
class Recover(MoveEffect):
    def use(self):
        if self.user.hp == self.user.stats.hp:
            self.fail()
        else:
            # Rounded up for some reason...
            amount = int(self.user.stats.hp / 2 + 0.5)
            self.user.change_hp(amount, message_class=messages.Recover)

@registry.put(37)
class TriAttack(SecondaryStatusMove):
    @property
    def effect_class(self):
        return self.field.random_choice([
                effects.Paralysis,
                effects.Burn,
                effects.Freeze,
            ], "Choose the Tri Attack effect")

@registry.put(53)
class Agility(UserStatChangeMove):
    stat_identifier = 'speed'
    delta = +2

@registry.put(71)
class IcyWind(TargetSecondaryStatChangeMove):
    stat_identifier = 'speed'
    delta = -1

@registry.put(95)
class LockOn(MoveEffect):
    def hit(self, hit):
        effect = self.user.give_effect(hit.target, effects.LockOn())
        if effect:
            self.field.message(messages.TakeAim, battler=self.user,
                    target=hit.target)

@registry.put(77)
class Confusion(MoveEffect):
    def do_secondary_effect(self, hit):
        if not hit.target.fainted:
            effect = self.user.give_effect(hit.target, effects.Confusion())
            if effect:
                self.field.message(messages.Confusion.Applied,
                        battler=effect.subject)

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

@registry.put(104)
class QuickAttack(MoveEffect):
    pass

@registry.put(255)
class Struggle(MoveEffect):
    def __init__(self, *args, **kwargs):
        super(Struggle, self).__init__(*args, **kwargs)
        self.type = None

    def hit(self, hit):
        super(Struggle, self).hit(hit)
        self.user.do_damage(self.user.stats.hp // 4,
                message_class=messages.Recoil)

@registry.put(253)
class MagnetRise(MoveEffect):
    def use(self):
        effect = self.user.give_effect_self(effects.MagnetRise())
        if effect:
            self.field.message.MagnetRise(battler=self.user)
        else:
            self.fail()

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
