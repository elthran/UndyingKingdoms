from undyingkingdoms.models.buildings import Building

generic_buildings = {'house': Building(base_name='house',
                                       class_name='house',
                                       class_name_plural='houses',
                                       total=25,
                                       workers_employed=0,
                                       gold_cost=35,
                                       wood_cost=25,
                                       stone_cost=0,
                                       output=1,
                                       description='Each {} adds +{} to your birth rate.'),
                     'field': Building(base_name='field',
                                       class_name='grain field',
                                       class_name_plural='grain fields',
                                       total=15,
                                       workers_employed=5,
                                       gold_cost=35,
                                       wood_cost=5,
                                       stone_cost=0,
                                       output=25,
                                       description='Each {} provides enough grain for {} people a day.'),
                     'pasture': Building(base_name='pasture',
                                         class_name='goat farm',
                                         class_name_plural='goat farms',
                                         total=15,
                                         workers_employed=15,
                                         gold_cost=35,
                                         wood_cost=5,
                                         stone_cost=0,
                                         output=25,
                                         description='Each {} can feed {} people a day, but excess dairy is lost.'),
                     'mill': Building(base_name='mill',
                                      class_name='lumber mill',
                                      class_name_plural='lumber mills',
                                      total=3,
                                      workers_employed=15,
                                      gold_cost=50,
                                      wood_cost=25,
                                      stone_cost=0,
                                      output=4,
                                      description='Each {} produces {} wood a day.'),
                     'mine': Building(base_name='mine',
                                      class_name='iron mine',
                                      class_name_plural='iron mines',
                                      total=1,
                                      workers_employed=25,
                                      gold_cost=40,
                                      wood_cost=20,
                                      stone_cost=0,
                                      output=2,
                                      description='Each {} produces {} iron a day.'),
                     'quarry': Building(base_name='quarry',
                                        class_name='stone quarry',
                                        class_name_plural='stone quarries',
                                        total=0,
                                        workers_employed=30,
                                        gold_cost=50,
                                        wood_cost=25,
                                        stone_cost=0,
                                        output=1,
                                        description='Each {} produces {} stone a day.'),
                     'fort': Building(base_name='fort',
                                      class_name='stronghold',
                                      class_name_plural='strongholds',
                                      total=0,
                                      workers_employed=25,
                                      gold_cost=100,
                                      wood_cost=75,
                                      stone_cost=15,
                                      output=7,
                                      description='Each {} adds +{}% to your county\'s defence value.'),
                     'stables': Building(base_name='stables',
                                         class_name='pony stables',
                                         class_name_plural='pony stables',
                                         total=0,
                                         workers_employed=15,
                                         gold_cost=40,
                                         wood_cost=20,
                                         stone_cost=5,
                                         output=10,
                                         description='Each {} lets your army return from battle {}% faster.'),
                     'guild': Building(base_name='guild',
                                       class_name='thieves\' den',
                                       class_name_plural='thieves\' dens',
                                       total=0,
                                       workers_employed=25,
                                       gold_cost=65,
                                       wood_cost=50,
                                       stone_cost=10,
                                       output=1,
                                       description="Each {} gives you {} additional spies to send on missions."),
                     'bank': Building(base_name='bank',
                                      class_name='vault',
                                      class_name_plural='vaults',
                                      total=0,
                                      workers_employed=5,
                                      gold_cost=60,
                                      wood_cost=30,
                                      stone_cost=5,
                                      output=8,
                                      description="Each {} gives you {} additional gold per day."),
                     'lair': Building(base_name='lair',
                                      class_name='lair',
                                      class_name_plural='lairs',
                                      total=0,
                                      workers_employed=50,
                                      gold_cost=300,
                                      wood_cost=200,
                                      stone_cost=125,
                                      output=1,
                                      description="Each {} allows you to capture and train {} monster.")
                     }
