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
    class Name(Message):
        registry_name = 'Paralysis.Name'
        message = "Paralysis"

    class Applied(Message):
        registry_name = 'Paralysis.Applied'
        message = "{battler} was paralyzed! It may be unable to attack!"
        battler = MessageArgument()

    class PreventUse(Message):
        registry_name = 'Paralysis.PreventUse'
        message = "{battler} is fully paralyzed! It can't move!"
        battler = MessageArgument()

class Burn(object):
    class Name(Message):
        registry_name = 'Burn.Name'
        message = "Burn"

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
    class Name(Message):
        registry_name = 'Freeze.Name'
        message = "Freeze"

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
    class Name(Message):
        registry_name = 'Confusion.Name'
        message = "Confusion"

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
        message = "{battler} snapped out of confusion!"
        battler = MessageArgument()

    class AlreadyPresent(Message):
        message = "{battler} is already confused!"
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

class AnnounceAirBalloon(Message):
    message = "{battler} floats in the air with its {item}!"
    battler = MessageArgument()
    item = MessageArgument()

class AirBalloonPopped(Message):
    # XXX: Item consumption
    message = "{battler}'s {item} popped!"
    battler = MessageArgument()
    item = MessageArgument()

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

class Sturdy(Message):
    message = "{battler} held on thanks to {ability}!"
    battler = MessageArgument()
    ability = MessageArgument()

class MagnetRise(Message):
    message = "{battler} levitated on electromagnetism!"
    battler = MessageArgument()

class MagnetRiseEnd(Message):
    message = "{battler}'s electromagnetism wore off!"
    battler = MessageArgument()

class TakeAim(Message):
    message = "{battler} took aim at {target}!"
    battler = MessageArgument()
    target = MessageArgument()

class Frisk(Message):
    message = "{frisker} frisked {battler} and found one {item}!"
    frisker = MessageArgument()
    battler = MessageArgument()
    ability = MessageArgument()
    item = MessageArgument()

class NaturalCure(Message):
    message = "{battler}'s {ability} cured its status!"
    battler = MessageArgument()
    ability = MessageArgument()

class AbilityPreventAilment(Message):
    message = "{battler}'s {ability} prevented the {ailment}!"
    battler = MessageArgument()
    ability = MessageArgument()
    ailment = MessageArgument()

class ColorChange(Message):
    message = "{battler}'s {ability} changes its type to {type}!"
    battler = MessageArgument()
    ability = MessageArgument()
    type = MessageArgument()

class AbilityBlocksHit(Message):
    message = "{battler}'s {ability} blocks the hit!"
    battler = MessageArgument()
    ability = MessageArgument()
    hit = MessageArgument()
