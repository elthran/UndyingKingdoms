from undyingkingdoms.models.magic import Magic

elf_spells = {'population_killer': Magic(name='population_killer',
                                         display_name='Arcane Fire',
                                         category='instant',
                                         targets='hostile',
                                         known=True,
                                         mana_cost=15,
                                         output=4,
                                         description='A blast of holy fire kills 6% of their population.'),
              'modify_birth_rate': Magic(name='modify_birth_rate',
                                         display_name='Ambrosia',
                                         category='aura',
                                         targets='self',
                                         known=True,
                                         mana_cost=20,
                                         mana_sustain=3,
                                         output=0.25,
                                         description='Increases your birth rate by 25% while active.')}
