from undyingkingdoms.models.technologies import Technology

goblin_technology = {'slavery': Technology(name='slavery',
                                           cost=1000,
                                           tier=2,
                                           max_level=1,
                                           description='Your slaves are 5 gold, 1 wood, and 1 iron cheaper.'),
                     'deathwish': Technology(name='deathwish',
                                             cost=1000,
                                             tier=2,
                                             max_level=1,
                                             description='Your berserkers have +1 attack.'),
                     'barbed arrows': Technology(name='barbed arrows',
                                                 cost=1000,
                                                 tier=2,
                                                 max_level=1,
                                                 description='Your bowmen get +1 defence.'),
                     'cross-breeding': Technology(name='cross-breeding',
                                                  cost=1000,
                                                  tier=2,
                                                  max_level=1,
                                                  description='Wolf riders get +3 attack.')
                     }
