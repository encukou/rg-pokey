#! /usr/bin/env python
# Encoding: UTF-8

import re
from fractions import Fraction

from regeneration.battle.effect import Effect

from regeneration.pokey import messages
from regeneration.pokey import effects
from regeneration.pokey.registry import EntityRegistry
from regeneration.pokey.orderkeys import (EndTurnOrder, DamageModifierOrder,
        AnnounceOrder, DamageReactionOrder)

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class ItemRegistry(EntityRegistry):
    def get_key(self, item):
        # XXX: The Gen.V items apparently don't have flags set properly
        if item: #  and any(f.identifier == 'holdable' for f in item.flags):
            if item.identifier in ('nugget', 'pearl', 'big-pearl'):
                return 'no-item'
            return super(ItemRegistry, self).get_key(item)
        else:
            return 'no-item'

item_effect_registry = ItemRegistry()
register = item_effect_registry.register

@register
def NoItem(item):
    return None

class ItemEffect(Effect):
    def __init__(self, item):
        self.item = item

class ChoiceItem(ItemEffect):
    def modify_stat(self, battler, value, stat):
        if battler is self.subject and stat.identifier == self.stat_identifier:
            return value * 3 // 2
        else:
            return value

    def move_used(self, move_effect):
        if (move_effect.user is self.subject and
                not self.subject.get_effect(effects.ChoiceLock)):
            self.subject.give_effect_self(effects.ChoiceLock(move_effect.move))

class TypeBoostItem(ItemEffect):
    @Effect.orderkey(DamageModifierOrder.item)
    def modify_base_power(self, hit, power):
        if (hit.user is self.subject and hit.type and
                hit.type.identifier == self.type_identifier):
            return power * 6 // 5
        else:
            return power

@register
class AirBalloon(ItemEffect, effects.Hovering):
    @Effect.orderkey(AnnounceOrder.item)
    def send_out(self, battler):
        if battler is self.subject:
            self.field.message.AnnounceAirBalloon(battler=battler,
                    item=self.item)

    @Effect.orderkey(DamageReactionOrder.target_item)
    def move_damage_done(self, hit):
        if hit.target is self.subject and hit.user is not self.subject:
            self.subject.item = None
            self.field.message.AirBalloonPopped(battler=self.subject,
                    item=self.item)

@register
class BlackBelt(TypeBoostItem):
    type_identifier = 'fighting'

@register
class Blackglasses(TypeBoostItem):
    type_identifier = 'dark'

@register
class Brightpowder(ItemEffect):
    def modify_accuracy(self, hit, accuracy):
        if hit.target is self.subject:
            return accuracy * Fraction(9, 10)
        else:
            return accuracy

@register
class Charcoal(TypeBoostItem):
    type_identifier = 'fire'

@register
class ChoiceBand(ChoiceItem):
    stat_identifier = 'attack'

@register
class ChoiceScarf(ChoiceItem):
    stat_identifier = 'speed'

@register
class ChoiceSpecs(ChoiceItem):
    stat_identifier = 'special-attack'

@register
class DragonFang(TypeBoostItem):
    type_identifier = 'dragon'

@register
class FlameOrb(ItemEffect):
    @EndTurnOrder.speed_key(EndTurnOrder.general, EndTurnOrder.orb)
    def end_turn(self, field):
        effect = self.subject.give_effect_self(effects.Burn(verbose=False))
        if effect:
            self.field.message(messages.Burn.ItemApplied,
                    battler=effect.subject, item=self.item)

@register
class HardStone(TypeBoostItem):
    type_identifier = 'rock'

@register
class Magnet(TypeBoostItem):
    type_identifier = 'electric'

@register
class MetalCoat(TypeBoostItem):
    type_identifier = 'steel'

@register
class MiracleSeed(TypeBoostItem):
    type_identifier = 'grass'

@register
class MysticWater(TypeBoostItem):
    type_identifier = 'water'

@register
class Nevermeltice(TypeBoostItem):
    type_identifier = 'ice'

@register
class OddIncense(TypeBoostItem):
    type_identifier = 'psychic'

@register
class PoisonBarb(TypeBoostItem):
    type_identifier = 'poison'

@register
class RazorClaw(ItemEffect):
    def critical_hit_stage(self, hit, stage):
        if hit.user is self.subject:
            return stage + 1
        else:
            return stage

@register
class RockIncense(TypeBoostItem):
    type_identifier = 'rock'

@register
class RoseIncense(TypeBoostItem):
    type_identifier = 'grass'

@register
class ShellBell(ItemEffect):
    @Effect.orderkey(DamageReactionOrder.user_item)
    def move_damage_done(self, hit):
        subject = self.subject
        if (hit.user is subject and hit.target is not subject and
                subject.hp < subject.stats.hp):
            heal_amount = (hit.damage // 8) or 1
            subject.change_hp(heal_amount, message_class=messages.ItemHeal,
                    item=self.item)

@register
class LaxIncense(ItemEffect):
    def modify_accuracy(self, hit, accuracy):
        if hit.target is self.subject:
            return accuracy * Fraction(19, 20)
        else:
            return accuracy

@register
class Leftovers(ItemEffect):
    @EndTurnOrder.speed_key(EndTurnOrder.general, EndTurnOrder.heal_item)
    def end_turn(self, field):
        if self.subject.hp < self.subject.stats.hp:
            self.subject.change_hp(self.subject.stats.hp // 16,
                    message_class=messages.ItemHeal, item=self.item)

@register
class WiseGlasses(ItemEffect):
    @Effect.orderkey(DamageModifierOrder.item)
    def modify_base_power(self, hit, power):
        if (hit.user is self.subject and
                hit.damage_class.identifier == 'special'):
            return power * 11 // 10
        else:
            return power
