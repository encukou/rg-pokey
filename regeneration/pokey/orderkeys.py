#! /usr/bin/env python
# Encoding: UTF-8

from functools import wraps

from regeneration.battle.effect import Effect
from regeneration.battle.orderkey import OrderKeys
from regeneration.battle import orderkeys

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class DamageModifierOrder(object):

    # Reference: http://www.smogon.com/dp/articles/damage_formula

    (helping_hand, item, charge, mud_sport, water_sport, user_ability,
        target_ability) = OrderKeys(7)

    burn, reflect, double, weather, flashfire = orderkeys.mod1.new_after(5)

    sturdy = orderkeys.mod3.new_after()

class EndTurnOrder(object):

    # Reference: http://www.smogon.com/forums/showthread.php?t=79340

    (effect_end, wish, weather, weather_heal_ability, gravity, general,
        future_sight, perish_song, trick_room) = checkpoints = OrderKeys(9)

    # effect_end
    (reflect, light_screen, mist, safeguard, tailwind,
            lucky_chant) = OrderKeys(6)

    # general
    (ingrain, aqua_ring, speed_boost_shed_skin, heal_item, leech_seed,
            status_damage, orb, curse, trap, bad_dreams, uproar, disable,
            encore, taunt, magnet_rise, heal_block, embargo, yawn, sticky_barb
        ) = OrderKeys(19)

    @staticmethod
    def speed_key(major_tier, minor_tier=None):
        """Decorator for end-of-turn effects.

        Sort by major tier, then the subject speed, then the minor tier
        """
        def key(effect):
            try:
                speed = effect.subject.stats.speed
            except AttributeError:
                return major_tier, minor_tier
            else:
                speed *= Effect.speed_factor(effect, 1)
                return major_tier, -speed, minor_tier
        return Effect.orderkey(key)

class SwitchInDamage(object):
    toxic_spikes, spikes, stealth_rock = OrderKeys(3)

class PreventOrder(object):
    (immobile, truant, disable, imprison, heal_block, confusion, flinch, taunt,
            gravity, attract, paralysis) = OrderKeys(11)
