from undyingkingdoms.models.buildings import Building

generic_buildings = {'house': Building(name='house',
                                       class_name='Unnamed',
                                       class_name_plural='Unnamed Plural',
                                       total=25,
                                       workers_employed=0,
                                       gold_cost=35,
                                       wood_cost=25,
                                       stone_cost=0,
                                       output=1,
                                       description='Each {} adds +{} to your birth rate.'),
                     'field': Building(name='field',
                                       class_name='Unnamed',
                                       class_name_plural='Unnamed Plural',
                                       total=15,
                                       workers_employed=5,
                                       gold_cost=35,
                                       wood_cost=5,
                                       stone_cost=0,
                                       output=25,
                                       description='Each {} provides enough grain for {} people a day.'),
                     'pasture': Building(name='pasture',
                                         class_name='Unnamed',
                                         class_name_plural='Unnamed Plural',
                                         total=15,
                                         workers_employed=15,
                                         gold_cost=35,
                                         wood_cost=5,
                                         stone_cost=0,
                                         output=45,
                                         description='Each {} can feed {} people a day, but excess dairy is lost.'),
                     'mill': Building(name='mill',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=3,
                                      workers_employed=15,
                                      gold_cost=50,
                                      wood_cost=25,
                                      stone_cost=0,
                                      output=4,
                                      description='Each {} produces {} wood a day.'),
                     'mine': Building(name='mine',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=1,
                                      workers_employed=25,
                                      gold_cost=40,
                                      wood_cost=20,
                                      stone_cost=0,
                                      output=2,
                                      description='Each {} produces {} iron a day.'),
                     'quarry': Building(name='quarry',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=0,
                                        workers_employed=30,
                                        gold_cost=50,
                                        wood_cost=25,
                                        stone_cost=0,
                                        output=1,
                                        description='Each {} produces {} stone a day.'),
                     'fort': Building(name='fort',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=0,
                                      workers_employed=25,
                                      gold_cost=100,
                                      wood_cost=75,
                                      stone_cost=15,
                                      output=7,
                                      description='Each {} adds +{}% to your county\'s defence value.'),
                     'stables': Building(name='stables',
                                         class_name='Unnamed',
                                         class_name_plural='Unnamed Plural',
                                         total=0,
                                         workers_employed=15,
                                         gold_cost=40,
                                         wood_cost=20,
                                         stone_cost=5,
                                         output=10,
                                         description='Each {} lets your army return from battle {}% faster.'),
                     'bank': Building(name='bank',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=0,
                                      workers_employed=5,
                                      gold_cost=60,
                                      wood_cost=30,
                                      stone_cost=5,
                                      output=8,
                                      description="Each {} gives you {} additional gold per day."),
                     'tavern': Building(name='tavern',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=0,
                                        workers_employed=25,
                                        gold_cost=65,
                                        wood_cost=50,
                                        stone_cost=10,
                                        output=1,
                                        description="Each {} gives you {} additional spy to send on missions."),
                     'lab': Building(name='lab',
                                     class_name='Unnamed',
                                     class_name_plural='Unnamed Plural',
                                     total=0,
                                     workers_employed=25,
                                     gold_cost=80,
                                     wood_cost=30,
                                     stone_cost=15,
                                     output=5,
                                     description="Not implemented. Useless."),
                     'arcane': Building(name='arcane',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=0,
                                        workers_employed=5,
                                        gold_cost=80,
                                        wood_cost=30,
                                        stone_cost=15,
                                        output=3,
                                        description="Not implemented. Useless."),
                     'lair': Building(name='lair',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=0,
                                      workers_employed=50,
                                      gold_cost=300,
                                      wood_cost=200,
                                      stone_cost=125,
                                      output=1,
                                      description="Each {} allows you to capture and train {} monster.")
                     }
