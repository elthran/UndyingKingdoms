from undyingkingdoms.models.technologies import Technology

merchant_technology = {
    'economics i': Technology(name='economics i',
                              cost=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'economics ii': Technology(name='economics ii',
                               cost=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'economics iii': Technology(name='economics iii',
                                cost=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
