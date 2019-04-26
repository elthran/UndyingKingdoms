from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    'alchemy i': Technology(name='alchemy i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'alchemy ii': Technology(name='alchemy ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'alchemy iii': Technology(name='alchemy iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
