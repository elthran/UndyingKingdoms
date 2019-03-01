from undyingkingdoms.models.technologies import Technology

human_technology = {'civic duty': Technology(name='civic duty',
                                             required=500,
                                             tier=1,
                                             max_level=1,
                                             description='Reduces upkeep cost of men-at-arms by 5 gold each.'),
                    'economics': Technology(name='economics',
                                            required=750,
                                            tier=2,
                                            max_level=1,
                                            description='Increases all gold income by 15%.')
                    }
