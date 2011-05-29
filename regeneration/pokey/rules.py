#! /usr/bin/env python
# Encoding: UTF-8

from regeneration.battle.battler import Battler as BaseBattler
from regeneration.battle.field import Field as BaseField
from regeneration.battle.rules import (Rules, ValidationClause,
    ValidationError, MonsterValidationError, MoveValidationError)

from regeneration.pokey import messages
from regeneration.pokey.monster import Monster
from regeneration.pokey.effects import MajorAilment
from regeneration.pokey.abilityeffects import ability_effect_registry

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class Battler(BaseBattler):
    forced_move = None

    def __init__(self, monster, spot, loader):
        self.generation = monster.generation
        super(Battler, self).__init__(monster, spot, loader)
        self.give_effect_self(MajorAilment.effect_for_code(self.status))

    def get_ability_effect(self):
        return ability_effect_registry[self.ability](self.ability)

class Field(BaseField):
    BattlerClass = Battler
    message_module = messages

class GenerationValidationClause(ValidationClause):
    MonsterClass = Monster

    def validate_monster(self, monster):
        super(GenerationValidationClause, self).validate_monster(monster)
        if monster.generation != self.rules.loader.generation:
            raise MonsterValidationError(
                    '%s is from a wrong generation' % monster)

    def validate_move(self, move):
        super(GenerationValidationClause, self).validate_move(move)
        if move.generation != self.rules.loader.generation:
            raise MoveValidationError('%s is from a wrong generation' % move)

class PokeyRules(Rules):
    MonsterClass = Monster
    FieldClass = Field

    default_clause_classes = Rules.default_clause_classes + [
            GenerationValidationClause]
