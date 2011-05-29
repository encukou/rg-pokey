#! /usr/bin/env python
# Encoding: UTF-8

from pokedex.db.tables import (Stat as _Stat, Ability as _Ability,
        Type as _Type, Item as _Item)

from regeneration.battle.messages import *

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

for cls in _Stat, _Ability, _Type, _Item:
    @multimethod(cls, object)
    def message_values(entity, trainer):
        return dict(
                name=entity.name,
                identifier=entity.identifier,
            )

class Trace(GainAbility):
    message = "{battler} traced {opponent}'s {ability}"
    battler = MessageArgument()
    ability = MessageArgument()
    opponent = MessageArgument()

class DownloadActivated(Message):
    message = "{battler}'s {ability} activated!"
    battler = MessageArgument()
    ability = MessageArgument()

class Paralysis(object):
    class Applied(Message):
        message = "{battler} was paralyzed! It may be unable to attack!"
        battler = MessageArgument()

    class PreventUse(Message):
        message = "{battler} is fully paralyzed! It can't move!"
        battler = MessageArgument()

class Burn(object):
    class Applied(Message):
        message = "{battler} was burned!"
        battler = MessageArgument()

    class Hurt(HPChange):
        message = "{battler} was hurt by its burn!"

class Freeze(object):
    class Applied(Message):
        message = "{battler} was frozen solid!"
        battler = MessageArgument()

    class PreventUse(Message):
        message = "{battler} is frozen solid!"
        battler = MessageArgument()

    class Heal(Message):
        message = "{battler} thawed out!"
        battler = MessageArgument()

class TwistedDimensions(Message):
    message = "{battler} twisted the dimensions!"
    battler = MessageArgument()

class NormalDimensions(Message):
    message = "The twisted dimensions returned to normal."

class Recoil(HPChange):
    message = "{battler} is hurt by recoil!"
