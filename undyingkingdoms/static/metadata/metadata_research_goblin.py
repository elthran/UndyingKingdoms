from undyingkingdoms.models.technologies import Technology

goblin_technology = {'slavery': Technology(name='slavery',
                                           required=1000,
                                           tier=2,
                                           max_level=1,
                                           description='Your unemployed citizens produce double the amount of excess labour.'),
                     'cross-breeding': Technology(name='cross-breeding',
                                                  required=1250,
                                                  tier=3,
                                                  max_level=1,
                                                  description='Wolf riders get an additional 2 attack points.')
                     }
