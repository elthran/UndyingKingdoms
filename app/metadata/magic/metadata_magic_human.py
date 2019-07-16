from app.models.magic import Magic

human_spells = {
    'population_killer': Magic(name='population_killer',
                               display_name='Incantation of Fire',
                               source='Human',
                               category='instant',
                               targets='hostile',
                               known=True,
                               mana_cost=15,
                               output=5,
                               description='A blasts of fire hits the enemy county, '
                                           'killing 5% of their populace.'),
    'modify_offensive_power': Magic(name='modify_offensive_power',
                                    display_name='Discipline',
                                    source='Human',
                                    category='aura',
                                    targets='self',
                                    known=True,
                                    mana_cost=5,
                                    mana_sustain=1,
                                    output=0.05,
                                    description='While active, your troops have +5% attack power.'),
    'modify_magic_disrupt': Magic(
        name='modify_magic_disrupt',
        display_name='Shield of Faith',
        source='Human',
        category='aura',
        targets='self',
        known=True,
        mana_cost=20,
        mana_sustain=2,
        output=40,
        description='While active, '
                    'you have a +40% chance of disrupting enemy spells.')
}
