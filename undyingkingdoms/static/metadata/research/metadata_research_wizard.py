from undyingkingdoms.models.technologies import Technology

wizard_technology = {
    'spellcrafting i': Technology(name='spellcrafting i',
                              cost=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'spellcrafting ii': Technology(name='spellcrafting ii',
                               cost=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'spellcrafting iii': Technology(name='spellcrafting iii',
                                cost=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
