from undyingkingdoms.models.magic import Magic

goblin_spells = {
    'population_killer': Magic(name='population_killer',
                               display_name='Green Fire',
                               source='Goblin',
                               category='instant',
                               targets='hostile',
                               known=True,
                               mana_cost=8,
                               output=3,
                               description='A blast of green fire kills 3% of their population.'),
    'modify_offensive_power': Magic(name='modify_offensive_power',
                                    display_name='Bloodlust',
                                    source='Goblin',
                                    category='timed',
                                    targets='self',
                                    known=True,
                                    mana_cost=30,
                                    duration=12,
                                    output=0.15,
                                    description='While active, all your troops have +15% attack power.'),
    'modify_magic_disrupt': Magic(
        name='modify_magic_disrupt',
        display_name='Magical Barrier',
        source='Goblin',
        category='aura',
        targets='self',
        known=True,
        mana_cost=20,
        mana_sustain=2,
        output=40,
        description='While active, '
                    'you have a +40% chance of disrupting enemy spells.')
}
