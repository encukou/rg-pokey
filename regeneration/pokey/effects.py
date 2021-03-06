#! /usr/bin/env python
# Encoding: UTF-8

from fractions import Fraction

from regeneration.battle.effect import Effect
from regeneration.battle.moveeffect import MoveEffect, Hit

from regeneration.pokey import orderkeys
from regeneration.pokey.orderkeys import EndTurnOrder, MoveHitsDoneOrder
from regeneration.pokey import messages

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class DaemonEffect(Effect):
    def _checkpoints(effect):
        for c in EndTurnOrder.checkpoints:
            yield c, EndTurnOrder.end_tier_effect, 0, 0, 0

    @Effect.orderkey(_checkpoints)
    def end_turn(self, field):
        if field.check_win():
            return True

class Ailment(Effect):
    def __init__(self, verbose=True):
        """Initializer

        Set verbose to false if the effect should be blocked quietly.
        If left true, a blocking effect will complain with a message like "But
        XYZ is burned already!" or "ABC prevents XYZ from being frozen!".
        """
        self.verbose = verbose
        super(Ailment, self).__init__()

    def message_values(self, trainer):
        return {
                'name': self.messages.Name.message,
                'class': self.messages.Name.registry_name,
            }

class MajorAilment(Ailment):
    class_by_code = {}
    immune_type_identifiers = ()

    # Reference: http://www.smogon.com/dp/articles/status

    def block_application(self, effect):
        if effect is self and (self.subject.get_effect(MajorAilment) or any(
                t.identifier in self.immune_type_identifiers for t in
                self.subject.types)):
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
        return cls.class_by_code[code](verbose=False)

    @classmethod
    def register(cls, code):
        def decorator(effect_class):
            cls.class_by_code[code] = effect_class
            effect_class.status_code = code
            return effect_class
        return decorator

    def message_values(self, trainer=None):
        return dict(
                effect_type=type(self).__name__,
            )

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

    @Effect.orderkey(orderkeys.PreventOrder.paralysis)
    def prevent_use(self, move_effect):
        subject = self.subject
        if move_effect.user is subject:
            if self.field.flip_coin(Fraction(1, 4), "Check full paralysis"):
                self.field.message(self.messages.PreventUse, battler=subject)
                return True

@MajorAilment.register('brn')
class Burn(MajorAilment):
    # XXX: Pokémon with the ability Leaf Guard (in bright sunlight) or Water
    # Veil are unaffected by burns.
    # XXX: Pokemon with Heatproof take only 6.25% damage per turn
    # XXX: When a Pokémon with the ability Magic Guard is burned, it does not
    # lose health, though its physical damage still drops.

    messages = messages.Burn
    immune_type_identifiers = ['fire']

    @Effect.orderkey(orderkeys.DamageModifierOrder.burn)
    def modify_move_damage(self, hit, damage):
        damage_class = hit.move_effect.damage_class
        if hit.user is self.subject and damage_class.identifier == 'physical':
            return damage // 2
        else:
            return damage

    @EndTurnOrder.speed_key(EndTurnOrder.status_damage)
    def end_turn(self, field):
        self.subject.do_damage(self.subject.stats.hp // 8 or 1,
                message_class=self.messages.Hurt)

@MajorAilment.register('frz')
class Freeze(MajorAilment):
    # XXX: Pokémon with the ability Magma Armor are immune to [...] freeze
    # No Pokémon can be frozen while the sun is bright.

    messages = messages.Freeze
    immune_type_identifiers = ['ice']

    @Effect.orderkey(orderkeys.PreventOrder.immobile)
    def prevent_use(self, move_effect):
        subject = self.subject
        if move_effect.user is subject:
            if (move_effect.move.flags.defrost or
                    self.field.flip_coin(Fraction(1, 5),
                            "Check for thawing out")):
                self.defrost()
            else:
                self.field.message(self.messages.PreventUse, battler=subject)
                return True

    @Effect.orderkey(orderkeys.MoveHitsDoneOrder.thaw)
    def move_hits_done(self, move_effect, hits):
        if (hits and move_effect.target is self.subject and
                move_effect.type and move_effect.type.identifier == 'fire'):
            self.defrost()

    def defrost(self):
        self.remove()
        self.field.message(self.messages.Heal, battler=self.subject)

@MajorAilment.register('psn')
class Poison(MajorAilment):
    # XXX: Dummy for now
    pass

class Confusion(Ailment):
    messages = messages.Confusion

    def block_application(self, effect):
        if effect is self and self.subject.get_effect(Confusion):
            if effect.verbose:
                self.field.message(messages.Confusion.AlreadyPresent,
                        battler=self.subject)
            return True

    def effect_applied(self, effect):
        if effect is self:
            self.counter = self.field.randint(2, 5, "Confusion duration")

    @Effect.orderkey(orderkeys.PreventOrder.confusion)
    def prevent_use(self, move_effect):
        subject = self.subject
        if move_effect.user is subject:
            self.counter -= 1
            if self.counter <= 0:
                self.field.message(messages.Confusion.Heal, battler=subject)
                self.remove()
            else:
                self.field.message(messages.Confusion.Tick, battler=subject)
                if self.field.flip_coin(Fraction(1, 2), "Confusion check"):
                    self.field.message(messages.Confusion.Hurt,
                            battler=subject)
                    fake_move_effect = self.ConfusionHurtEffect(subject)
                    fake_move_effect.do_damage(Hit(fake_move_effect, subject))
                    return True

    class ConfusionHurtEffect(MoveEffect):
        def __init__(self, user):
            self.move = None
            self.power = 40
            self.field = user.field
            self.target = self.user = user
            self.accuracy = self.type = self.secondary_effect_chance = None
            self.damage_class = user.field.loader.load_damage_class('physical')
            self.flags = self.flags.union([self.ppless])

        @property
        def name(self):
            return '<confusion>'

        def determine_critical_hit(self, hit):
            hit.is_critical = False

        def message_values(self, trainer):
            return {
                    'name': '<confusion>',
                    'target': self.target.message_values(trainer),
                }

class UnblockableMove(Effect):
    def disable_callback(self, effect, callback_name, arguments):
        if callback_name in ('prevent_use', 'prevent_hit'):
            return True

class TwistedDimensions(Effect):
    def effect_applied(self, effect):
        if effect is self:
            self.counter = 5

    def speed_factor(self, field, speed_factor):
        return -1

    @EndTurnOrder.speed_key(EndTurnOrder.trick_room_end)
    def end_turn(self, field):
        self.counter -= 1
        if self.counter <= 0:
            self.remove()
            self.field.message(messages.NormalDimensions)

class ChoiceLock(Effect):
    def __init__(self, locked_move):
        self.locked_move = locked_move

    def prevent_move_selection(self, command):
        if (command.battler is self.subject and
                command.move != self.locked_move):
            return True

class Hovering(Effect):
    def modify_effectivity(self, hit, effectivity):
        if (hit.target is self.subject and hit.type and
                hit.type.identifier == 'ground'):
            return 0
        else:
            return effectivity

class MagnetRise(Hovering):
    def __init__(self):
        self.turns_left = 5

    @EndTurnOrder.speed_key(EndTurnOrder.magnet_rise_end)
    def end_turn(self, field):
        self.turns_left -= 1
        if self.turns_left <= 0:
            self.remove()
            if not self.subject.get_effect(MagnetRise):
                self.field.message.MagnetRiseEnd(battler=self.subject)

class LockOn(Effect):
    def __init__(self):
        self.turns_left = 2

    @EndTurnOrder.speed_key(EndTurnOrder.quiet)
    def end_turn(self, field):
        self.turns_left -= 1
        if self.turns_left <= 0:
            self.remove()

    def ensure_hit(self, hit):
        if hit.target is self.subject and hit.user is self.inducer:
            return True
