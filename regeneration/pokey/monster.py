#! /usr/bin/env python
# Encoding: UTF-8

import yaml
import random
import functools
from fractions import Fraction

from pokedex.db import tables
from pokedex.lookup import PokedexLookup

from regeneration.battle.monster import Monster as BaseMonster

from regeneration.pokey.move import Move

__copyright__ = 'Copyright 2009-2011, Petr Viktorin'
__license__ = 'MIT'
__email__ = 'encukou@gmail.com'

class Monster(BaseMonster):
    def __init__(self, form, level, loader, rand=random, **kwargs):
        self.nature = rand.choice(loader.natures)

        self.generation = loader.generation
        super(Monster, self).__init__(form, level, loader, **kwargs)

    @property
    def MoveClass(self):
        return functools.partial(Move, generation=self.generation)

    def get_kind(self, form):
        return form.pokemon

    def recalculate_stats(self):
        missing_hp = self.stats.hp - self.hp
        for stat in self.genes:
            (pstat,) = (
                    pstat for pstat in self.kind.stats
                    if pstat.stat.name == stat.name
                )
            base = pstat.base_stat
            gene = self.genes[stat]
            effort = self.effort[stat]
            level = self.level
            result = ((2 * base + gene + (effort // 4)) * level // 100 + 5)
            if stat.identifier == 'hp':
                result += level + 5
            else:
                nature_modifier = 1
                if self.nature.increased_stat is pstat.stat:
                    nature_modifier += Fraction(1, 10)
                if self.nature.decreased_stat is pstat.stat:
                    nature_modifier -= Fraction(1, 10)
                result = int(result * nature_modifier)
            self.stats[stat] = result
        self.hp = self.stats.hp - missing_hp
        if self.hp < 0:
            self.hp = 0

    def default_moves(self, loader):
        query = loader.session.query(tables.Move)
        query = query.join(tables.Move.pokemon_moves)
        query = query.join(tables.PokemonMove.version_group)
        query = query.filter(tables.PokemonMove.pokemon_id == self.kind.id)
        query = query.filter(tables.VersionGroup.generation_id ==
                self.generation)
        query = query.filter(tables.PokemonMove.level <= self.level)
        query = query.order_by(tables.PokemonMove.level.desc())
        query = query.distinct()
        return list(query[:4])

if __name__ == '__main__':
    # Generate a random monster
    from regeneration.pokey.loader import default_loader
    lookup = PokedexLookup(session=default_loader.session)
    species = lookup.lookup('pokemon_species:random')
    form = random.choice(species[0].object.forms)
    monster = Monster(form, random.randint(1, 100), default_loader)
    print yaml.safe_dump(monster.save())
