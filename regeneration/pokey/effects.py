#! /usr/bin/env python
# Encoding: UTF-8

from fractions import Fraction

from regeneration.battle.effect import Effect

from regeneration.pokey import orderkeys
from regeneration.pokey.orderkeys import EndTurnOrder
from regeneration.pokey import messages

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class MajorAilment(Effect):
    class_by_code = {}

    # Reference: http://www.smogon.com/dp/articles/status

    def block_application(self, effect):
        if effect is self and self.subject.get_effect(MajorAilment):
            return True

    def effect_applied(self, effect):
        if effect is self:
            self.subject.status = self.status_code

    def effect_removed(self, effect):
        if effect is self:
            self.subject.status = 'ok'

    @classmethod
    def effect_for_code(cls, code):
        if code == 'ok':
            return None
        return cls.class_by_code[code]()

    @classmethod
    def register(cls, code):
        def decorator(effect_class):
            cls.class_by_code[code] = effect_class
            effect_class.status_code = code
            return effect_class
        return decorator

@MajorAilment.register('par')
class Paralysis(MajorAilment):
    # XXX: Pokémon with the abilities Limber and Leaf Guard (during bright
    # sunlight) are immune to paralysis.
    # XXX: Pokemon with the ability Magic Guard are never fully paralyzed; they
    # do, however, suffer from the Speed drop.

    messages = messages.Paralysis

    def modify_stat(self, battler, value, stat):
        if battler is self.subject and stat.identifier == 'speed':
            return value // 4
        else:
            return value

    def prevent_use(self, move_effect):
        subject = self.subject
        if move_effect.user is subject:
            if self.field.flip_coin(Fraction(1, 4), "Check full paralysis"):
                self.field.message(self.messages.PreventUse, battler=subject)
                return True

@MajorAilment.register('brn')
class Burn(MajorAilment):
    # XXX: Fire-type Pokémon, as well as Pokémon with the ability Leaf Guard
    # (in bright sunlight) or Water Veil are unaffected by burns.
    # XXX: Pokemon with Heatproof take only 6.25% damage per turn
    # XXX: When a Pokémon with the ability Magic Guard is burned, it does not
    # lose health, though its physical damage still drops.

    messages = messages.Burn

    @Effect.orderkey(orderkeys.DamageModifierOrder.burn)
    def modify_move_damage(self, target, damage, hit):
        damage_class = hit.move_effect.damage_class
        if hit.user is self.subject and damage_class.identifier == 'physical':
            return damage // 2
        else:
            return damage

    @EndTurnOrder.speed_key(EndTurnOrder.general, EndTurnOrder.status_damage)
    def end_turn(self, field):
        self.subject.do_damage(self.subject.stats.hp // 8,
                message_class=self.messages.Hurt)

@MajorAilment.register('frz')
class Freeze(MajorAilment):
    # XXX: Pokémon with the ability Magma Armor are immune to [...] freeze
    # XXX: no freezing Ice-types
    # No Pokémon can be frozen while the sun is bright.

    messages = messages.Freeze

    def prevent_use(self, move_effect):
        subject = self.subject
        if move_effect.user is subject:
            if self.field.flip_coin(Fraction(1, 5), "Check for thawing out"):
                self.remove()
                self.field.message(self.messages.Heal, battler=subject)
            else:
                self.field.message(self.messages.PreventUse, battler=subject)
                return True

class TwistedDimensions(Effect):
    def effect_applied(self, effect):
        if effect is self:
            self.counter = 5

    def speed_factor(self, field, speed_factor):
        return -1

    @EndTurnOrder.speed_key(EndTurnOrder.trick_room)
    def end_turn(self, field):
        self.counter -= 1
        if self.counter <= 0:
            self.remove()
            self.field.message(messages.NormalDimensions)

