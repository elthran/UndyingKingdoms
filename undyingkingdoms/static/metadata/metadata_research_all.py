from undyingkingdoms.models.technologies import Technology

generic_technology = {'agriculture': Technology(name='agriculture',
                                                required=600,
                                                max_level=3,
                                                description='+50% bonus to all grain production within your county.'),
                      'animal husbandry': Technology(name='animal husbandry',
                                                     required=600,
                                                     max_level=3,
                                                     description='+50% bonus to all dairy production within your county.'),
                      'steel': Technology(name='steel',
                                          required=1250,
                                          max_level=3,
                                          description='+20% Attack Power bonus to all offensive invasions you perform.'),
                      'engineering': Technology(name='engineering',
                                                required=200,
                                                max_level=3,
                                                description='+1 building can be built each day.')
                      }
