from undyingkingdoms.models.technologies import Technology

goblin_technology = {'slavery': Technology(name='slavery',
                                           required=1000,
                                           tier=2,
                                           max_level=1,
                                           description='Your slaves are 5 gold, 1 wood, and 1 iron cheaper.'),
                     'bloodlust': Technology(name='bloodlust',
                                             required=1000,
                                             tier=2,
                                             max_level=1,
                                             description='Your berserkers have +1 attack.'),
                     'barbed arrows': Technology(name='barbed arrows',
                                                 required=1000,
                                                 tier=2,
                                                 max_level=1,
                                                 description='Your bowmen get +1 defence.'),
                     'cross-breeding': Technology(name='cross-breeding',
                                                  required=1000,
                                                  tier=2,
                                                  max_level=1,
                                                  description='Wolf riders get +3 attack.')
                     }
