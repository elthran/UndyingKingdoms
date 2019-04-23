from undyingkingdoms.models.magic import Magic

elf_spells = {'population_killer_tier_1': Magic(name='population_killer_tier_1',
                                                display_name='arcane fire',
                                                category='instant',
                                                targets='hostile',
                                                known=True,
                                                mana_cost=15,
                                                description='A blast of holy fire hits the enemy county, killing some their populace.'),
              'ambrosia': Magic(name='ambrosia', display_name='gfhgf',
                                category='aura',
                                targets='self',
                                known=True,
                                mana_cost=20,
                                mana_sustain=2,
                                description='While active, your birth rate increase by 50%.')}
