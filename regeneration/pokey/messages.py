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
        registry_name = 'Paralysis.Applied'
        message = "{battler} was paralyzed! It may be unable to attack!"
        battler = MessageArgument()

    class PreventUse(Message):
        registry_name = 'Paralysis.PreventUse'
        message = "{battler} is fully paralyzed! It can't move!"
        battler = MessageArgument()

class Burn(object):
    class Applied(Message):
        registry_name = 'Burn.Applied'
        message = "{battler} was burned!"
        battler = MessageArgument()

    class ItemApplied(Applied):
        registry_name = 'Burn.ItemApplied'
        message = "{battler}'s {item} activated!"
        item = MessageArgument()

    class Hurt(HPChange):
        registry_name = 'Burn.Hurt'
        message = "{battler} was hurt by its burn!"

class Freeze(object):
    class Applied(Message):
        registry_name = 'Freeze.Applied'
        message = "{battler} was frozen solid!"
        battler = MessageArgument()

    class PreventUse(Message):
        registry_name = 'Freeze.PreventUse'
        message = "{battler} is frozen solid!"
        battler = MessageArgument()

    class Heal(Message):
        registry_name = 'Freeze.Heal'
        message = "{battler} thawed out!"
        battler = MessageArgument()

class Confusion(object):
    class Applied(Message):
        registry_name = 'Confusion.Applied'
        message = "{battler} was confused!"
        battler = MessageArgument()

    class Hurt(Message):
        registry_name = 'Confusion.Hurt'
        message = "{battler} hurt itself in its confusion!"
        battler = MessageArgument()

    class Tick(Message):
        registry_name = 'Confusion.Tick'
        message = "{battler} is confused!"
        battler = MessageArgument()

    class Heal(Message):
        registry_name = 'Confusion.Heal'
        message = "{battler} cnapped out of confusion!"
        battler = MessageArgument()

class TwistedDimensions(Message):
    message = "{battler} twisted the dimensions!"
    battler = MessageArgument()

class NormalDimensions(Message):
    message = "The twisted dimensions returned to normal."

class Recoil(HPChange):
    message = "{battler} is hurt by recoil!"

class ItemHeal(HPChange):
    message = "{battler}'s {item} restored its HP a little!"
    item = MessageArgument()

class ConvertedType(Message):
    message = "{battler} transformed to the {new_type} type!"
    battler = MessageArgument()
    new_type = MessageArgument()
    moveeffect = MessageArgument()

class AnnouncePressure(Message):
    message = "{battler} is exerting its {ability}!"
    battler = MessageArgument()
    ability = MessageArgument()

class ShedSkin(Message):
    message = "{battler} shed its skin!"
    battler = MessageArgument()

class Recover(HPChange):
    message = "{battler} regained health!"

class Synchronize(Message):
    message = "{synchronizer}'s {ability} also changes {battler}'s status!"
    synchronizer = MessageArgument()
    battler = MessageArgument()
    effect = MessageArgument()
    ability = MessageArgument()
