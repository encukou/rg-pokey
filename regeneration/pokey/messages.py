#! /usr/bin/env python
# Encoding: UTF-8

from pokedex.db.tables import Stat as _Stat, Ability as _Ability

from regeneration.battle.messages import *

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

@multimethod(_Stat, object)
def message_values(stat, trainer):
    return dict(
            name=stat.name,
            identifier=stat.identifier,
        )

@multimethod(_Ability, object)
def message_values(ability, trainer):
    return dict(
            name=ability.name,
            identifier=ability.identifier,
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
