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

    # Checkpoints: at the end of every tier, these are run
    checkpoints = OrderKeys()

    def new_tier(num=None, checkpoints=checkpoints):
        base = checkpoints.new_last()
        if num is None:
            return base, OrderKeys().new_last()
        else:
            return ((base, key) for key in OrderKeys(num))

    # This is for "quiet" effects; ones that don't affect anything else
    quiet = new_tier()

    # 1.0 weather ends
    weather_end = new_tier()
    # 2.0 Sandstorm damage, Hail damage, Rain Dish, Dry Skin, Ice Body
    weather_damage = new_tier()
    # 3.0 Future Sight, Doom Desire
    future_sight = new_tier()
    # 4.0 Wish
    wish = new_tier()
    # 5.0 Fire Pledge + Grass Pledge damage
    # 5.1 Shed Skin, Hydration, Healer
    # 5.2 Leftovers, Black Sludge
    burning_field, ability_heal, item_heal = new_tier(3)
    # 6.0 Aqua Ring
    aqua_ring = new_tier()
    # 7.0 Ingrain
    ingrain = new_tier()
    # 8.0 Leech Seed
    leech_seed = new_tier()
    # 9.0 (bad) poison damage, burn damage, Nightmare, Poison Heal
    status_damage = new_tier()
    # 10.0 Curse (from a Ghost-type)
    curse = new_tier()
    # 11.0 Bind, Wrap, Fire Spin, Clamp, Whirlpool, Sand Tomb, Magma Storm
    trap_damage = new_tier()
    # 12.0 Taunt ends
    taunt_end = new_tier()
    # 13.0 Encore ends
    encore_end = new_tier()
    # 14.0 Disable ends, Cursed Body ends
    disable_cb_end = new_tier()
    # 15.0 Magnet Rise ends
    magnet_rise_end = new_tier()
    # 16.0 Telekinesis ends
    telekinesis_end = new_tier()
    # 17.0 Heal Block ends
    heal_block_end = new_tier()
    # 18.0 Embargo ends
    embargo_end = new_tier()
    # 19.0 Yawn
    yawn = new_tier()
    # 20.0 Perish Song
    perish_song = new_tier()
    # 21.0 Reflect ends
    # 21.1 Light Screen ends
    # 21.2 Safeguard ends
    # 21.3 Mist ends
    # 21.4 Tailwind ends
    # 21.5 Lucky Chant ends
    # 21.6 Water Pledge + Fire Pledge ends, Fire Pledge + Grass Pledge ends
    #    Grass Pledge + Water Pledge ends
    (reflect_end, lightscreen_end, safeguard_end, mist_end, tailwind_end,
        lucky_chant_end, pledge_end) = new_tier(7)
    # 22.0 Gravity ends
    gravity_end = new_tier()
    # 23.0 Trick Room ends
    trick_room_end = new_tier()
    # 24.0 Wonder Room ends
    wonder_room_end = new_tier()
    # 25.0 Magic Room ends
    magic_room_end = new_tier()
    # 26.0 Uproar message
    # 26.1 Speed Boost, Bad Dreams, Harvest, Moody
    # 26.2 Toxic Orb activation, Flame Orb activation, Sticky Barb
    uproar_message, ability_effect, item_activation = new_tier(3)
    # 27.0 Zen Mode
    zen_mode = new_tier()
    # 28.0 Pokémon is switched in (if previous Pokémon fainted)
    # 28.1 Healing Wish, Lunar Dance
    # 28.2 Spikes, Toxic Spikes, Stealth Rock (hurt in the order they are
    #    first used)

    del new_tier

    tier_effect, end_tier_effect = OrderKeys(2)

    @staticmethod
    def speed_key(major_minor):
        """Decorator for end-of-turn effects.

        Sort by major tier, then the subject speed, then the minor tier
        """
        major_tier, minor_tier = major_minor
        def key(effect):
            try:
                speed = effect.subject.stats.speed
            except AttributeError:
                return major_tier, minor_tier
            else:
                speed *= Effect.speed_factor(effect, 1)
                return major_tier, EndTurnOrder.tier_effect, -speed, minor_tier
        return Effect.orderkey(key)

class SwitchInDamage(object):
    toxic_spikes, spikes, stealth_rock = OrderKeys(3)

class PreventOrder(object):
    (immobile, truant, disable, imprison, heal_block, confusion, flinch, taunt,
            gravity, attract, paralysis) = OrderKeys(11)

class AnnounceOrder(object):
    # XXX: Is it really true?
    item, ability = OrderKeys(2)

class DamageReactionOrder(object):
    # XXX: Is it really true?
    status, user_item, target_item, target_ability = OrderKeys(4)
