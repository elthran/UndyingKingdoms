from undyingkingdoms.models.magic import Magic

warlord_spells = {
    'modify_offensive_power': Magic(name='modify_offensive_power',
                                    display_name='Heart of War',
                                    source='Warlord',
                                    category='aura',
                                    targets='friendly',
                                    known=True,
                                    mana_cost=30,
                                    mana_sustain=2,
                                    output=0.25,
                                    description='While active, all your troops have +25% attack power.'),
'convert_citizens_into_peasants': Magic(name='convert_citizens_into_peasants',
                                    display_name='Muster for Battle',
                                    source='Warlord',
                                    category='instant',
                                    targets='self',
                                    known=True,
                                    mana_cost=30,
                                    output=25,
                                    description='Instantly convert up to 25 citizens into basic warriors.')
}
