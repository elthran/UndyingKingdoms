from undyingkingdoms.models.technologies import Technology

wizard_technology = {
    'spellcrafting i': Technology(name='spellcrafting i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'spellcrafting ii': Technology(name='spellcrafting ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'spellcrafting iii': Technology(name='spellcrafting iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
