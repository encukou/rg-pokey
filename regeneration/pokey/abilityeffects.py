#! /usr/bin/env python
# Encoding: UTF-8

from fractions import Fraction

from regeneration.battle.effect import Effect

from regeneration.pokey.registry import EntityRegistry
from regeneration.pokey import effects
from regeneration.pokey import orderkeys

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

ability_effect_registry = EntityRegistry()
register = ability_effect_registry.register

class AbilityEffect(Effect):
    def __init__(self, ability):
        self.ability = ability

class AilmentPreventingAbility(AbilityEffect):
    def block_application(self, effect):
        if effect.subject is self.subject and isinstance(effect,
                self.effect_class):
            return True

    def effect_applied(self, applied_effect):
        if applied_effect is self:
            removed_effect = self.subject.get_effect(self.effect_class)
            if removed_effect:
                removed_effect.remove()

class TypeBoostAbility(AbilityEffect):
    @Effect.orderkey(orderkeys.DamageModifierOrder.user_ability)
    def modify_base_power(self, hit, power):
        if (hit.type and hit.type.identifier == self.type_identifier and
                hit.user is self.subject and
                hit.user.hp * 3 <= hit.user.stats.hp):
            return power * 3 // 2
        else:
            return power

@register
class Blaze(TypeBoostAbility):
    type_identifier = 'fire'

@register
class Download(AbilityEffect):
    @Effect.orderkey(orderkeys.AnnounceOrder.ability)
    def send_out(self, battler):
        if battler is self.subject:
            self.field.message.DownloadActivated(battler=battler,
                    ability=self.ability)
            defense_sum = sum(b.stats.defense for b in battler.opponents)
            spdef_sum = sum(b.stats.special_defense for b in battler.opponents)
            if defense_sum < spdef_sum:
                raised_stat = self.field.loader.load_stat('attack')
            else:
                raised_stat = self.field.loader.load_stat('special-attack')
            battler.change_stat(raised_stat, +1, verbose=True)

@register
class Levitate(AbilityEffect, effects.Hovering):
    pass

@register
class Limber(AilmentPreventingAbility):
    effect_class = effects.Paralysis

@register
class Overgrow(TypeBoostAbility):
    type_identifier = 'grass'

@register
class OwnTempo(AilmentPreventingAbility):
    effect_class = effects.Confusion

@register
class Pressure(AbilityEffect):
    @Effect.orderkey(orderkeys.AnnounceOrder.ability)
    def send_out(self, battler):
        if battler is self.subject:
            self.field.message.AnnouncePressure(battler=battler,
                    ability=self.ability)

    def pp_reduction(self, moveeffect, pp_reduction):
        if self.subject in moveeffect.targets:
            return pp_reduction + 1
        else:
            return pp_reduction

@register
class ShedSkin(AbilityEffect):
    @orderkeys.EndTurnOrder.speed_key(
            orderkeys.EndTurnOrder.general,
            orderkeys.EndTurnOrder.speed_boost_shed_skin)
    def end_turn(self, field):
        ailment = self.subject.get_effect(effects.MajorAilment)
        if (ailment and
                self.field.flip_coin(Fraction(3, 10), 'Shed skin check')):
            self.field.message.ShedSkin(battler=self.subject)
            ailment.remove()

@register
class ShieldDust(AbilityEffect):
    def modify_secondary_chance(self, hit, chance):
        if hit.target is self.subject:
            return 0
        else:
            return chance

@register
class Sturdy(AbilityEffect):
    @Effect.orderkey(orderkeys.DamageModifierOrder.sturdy)
    def modify_move_damage(self, hit, damage):
        target = hit.target
        if (target is self.subject and target.hp >= target.stats.hp and
                damage >= target.hp):
            self.field.message.Sturdy(battler=target, ability=self.ability)
            return target.hp - 1
        else:
            return damage

@register
class Swarm(TypeBoostAbility):
    type_identifier = 'bug'

@register
class Synchronize(AbilityEffect):
    def effect_applied(self, effect):
        classes = effects.Burn, effects.Paralysis, effects.Poison
        if effect.subject is self.subject and isinstance(effect, classes):
            effect_class = type(effect)
            effect = self.subject.give_effect(effect.inducer, effect_class())
            if effect:
                self.field.message.Synchronize(
                        synchronizer=self.subject,
                        battler=effect.subject,
                        effect=effect,
                        ability=self.ability,
                    )
                self.field.message(effect.messages.Applied,
                        battler=effect.subject)


@register
class Trace(AbilityEffect):
    @Effect.orderkey(orderkeys.AnnounceOrder.ability)
    def send_out(self, battler):
        # XXX: This ability cannot copy Multitype (or Trace)
        if battler is self.subject:
            opponents = [o for o in battler.opponents if
                    o.ability.identifier != 'trace']
            if opponents:
                opponent = self.field.random_choice(opponents,
                        "Random opponent for Trace")
                battler.ability = opponent.ability
                self.field.message.Trace(battler=battler,
                        ability=opponent.ability,
                        opponent=opponent)
                try:
                    send_out = battler.ability_effect.send_out
                except AttributeError:
                    pass
                else:
                    send_out(battler)

@register
class Technician(AbilityEffect):
    @Effect.orderkey(orderkeys.DamageModifierOrder.user_ability)
    def modify_base_power(self, hit, power):
        if hit.user is self.subject and power <= 60:
            return power * 3 // 2
        else:
            return power
