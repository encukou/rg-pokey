#! /usr/bin/env python
# Encoding: UTF-8

from regeneration.battle.effect import Effect

from regeneration.pokey.registry import EntityRegistry
from regeneration.pokey import orderkeys

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

ability_effect_registry = EntityRegistry()
register = ability_effect_registry.register

class AbilityEffect(Effect):
    def __init__(self, ability):
        self.ability = ability

@register
class Download(AbilityEffect):
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
            battler.raise_stat(raised_stat, +1, verbose=True)

@register
class Swarm(AbilityEffect):
    @Effect.orderkey(orderkeys.DamageModifierOrder.user_ability)
    def modify_base_power(self, hit, power):
        if (hit.type and hit.type.identifier == 'bug' and
                hit.user is self.subject and
                hit.user.hp * 3 <= hit.user.stats.hp):
            return power * 3 // 2
        else:
            return power

@register
class Trace(AbilityEffect):
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
