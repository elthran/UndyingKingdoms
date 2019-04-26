from undyingkingdoms.models.technologies import Technology

warlord_technology = {
    'tactician i': Technology(name='tactician i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'tactician ii': Technology(name='tactician ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'tactician iii': Technology(name='tactician iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
