from undyingkingdoms.models.magic import Magic

generic_spells = {
    'instant_happiness': Magic(
        name='instant_happiness',
        display_name='Inspire',
        category='instant',
        targets='self',
        known=True,
        mana_cost=25,
        output=5,
        description='Adds +5 happiness to your county.'
    ),
    'summon_golem': Magic(
        name='summon_golem',
        display_name='golem',
        category='instant',
        targets='self',
        known=True,
        mana_cost=50,
        description='Summon a golem to join your army (Not yet implemented).'
    ),
    'modify_death_rate': Magic(
        name='modify_death_rate',
        display_name='modify_death_rate',
        category='timed',
        targets='hostile',
        known=True,
        mana_cost=30,
        duration=12,
        output=0.5,
        description='Adds a disease to an enemy county for 12 days. '
                    'While diseased, their people die 50% more quickly.'
    ),
    'modify_grain_rate': Magic(
        name='modify_grain_rate',
        display_name='modify_grain_rate',
        category='aura',
        targets='friendly',
        known=True,
        mana_cost=35,
        mana_sustain=2,
        output=0.5,
        description='Pastures produce +50% grain while this spell is in effect.'
    ),
    'modify_magic_disrupt': Magic(
        name='modify_magic_disrupt',
        display_name='modify_magic_disrupt',
        category='aura',
        targets='self',
        known=True,
        mana_cost=20,
        mana_sustain=2,
        output=40,
        description='While active, '
                    'you have a +40% chance of disrupting enemy spells.'
    )
}
