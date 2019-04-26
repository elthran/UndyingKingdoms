from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    'engineering i': Technology(name='engineering i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'engineering ii': Technology(name='engineering ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'engineering iii': Technology(name='engineering iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
