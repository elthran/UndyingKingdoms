from app.models.magic import Magic

wizard_spells = {
    'archer_killer': Magic(name='archer_killer',
                           display_name='Fire Rain',
                           source='Wizard',
                           category='instant',
                           targets='hostile',
                           known=True,
                           mana_cost=20,
                           output=5,
                           description='Fire rains upon the enemy fortifications, '
                                       'killing five of their defenders.'),
    'modify_grain_rate': Magic(
        name='modify_grain_rate',
        display_name='Nature\'s Blessing',
        source='Wizard',
        category='aura',
        targets='friendly',
        known=True,
        mana_cost=35,
        mana_sustain=2,
        output=0.5,
        description='Pastures produce +50% grain while this spell is in effect.'
    ),
    'summon_tier_1': Magic(
        name='summon_tier_1',
        display_name='Summon Elemental',
        source='Wizard',
        category='instant',
        targets='self',
        known=True,
        mana_cost=10,
        output=3,
        description='Summon 3 Elementals to join your army.'
    )
}
