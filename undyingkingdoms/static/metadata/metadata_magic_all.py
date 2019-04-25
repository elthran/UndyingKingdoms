from undyingkingdoms.models.magic import Magic

generic_spells = {
    'summon_golem': Magic(
        name='summon_golem',
        display_name='golem',
        source='generic',
        category='instant',
        targets='self',
        known=True,
        mana_cost=50,
        description='Summon a golem to join your army (Not yet implemented).'
    )
}
