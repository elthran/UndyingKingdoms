from undyingkingdoms.models.technologies import Technology

diplomat_technology = {
    'diplomacy i': Technology(name='diplomacy i',
                              cost=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'diplomacy ii': Technology(name='diplomacy ii',
                               cost=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'diplomacy iii': Technology(name='diplomacy iii',
                                cost=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
