from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    'blessings i': Technology(name='blessings i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'blessings ii': Technology(name='blessings ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'blessings iii': Technology(name='blessings iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
