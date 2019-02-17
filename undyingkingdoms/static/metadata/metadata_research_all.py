from undyingkingdoms.models.technologies import Technology

generic_technology = {'agriculture': Technology(name='agriculture',
                                                required=500,
                                                description='Researching this technology grants a +50% bonus to all grain production within your county.'),
                      'animal husbandry': Technology(name='animal husbandry',
                                                     required=750,
                                                     description='Researching this technology grants a +100% bonus to all dairy production within your county.')
                      }
