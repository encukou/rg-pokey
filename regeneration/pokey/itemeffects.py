#! /usr/bin/env python
# Encoding: UTF-8

import re
from fractions import Fraction

from regeneration.battle.effect import Effect

from regeneration.pokey.registry import EntityRegistry

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class ItemRegistry(EntityRegistry):
    def get_key(self, item):
        if any(f.identifier == 'holdable' for f in item.flags):
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

@register
class Brightpowder(ItemEffect):
    def modify_accuracy(self, hit, accuracy):
        if hit.target is self.subject:
            return accuracy * Fraction(9, 10)
        else:
            return accuracy
