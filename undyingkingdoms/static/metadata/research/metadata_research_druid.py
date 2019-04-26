from undyingkingdoms.models.technologies import Technology

druid_technology = {
    'nature i': Technology(name='nature i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'nature ii': Technology(name='nature ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'nature iii': Technology(name='nature iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
