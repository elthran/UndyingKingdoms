from undyingkingdoms.models.buildings import Building

generic_buildings = {'house': Building(name='house',
                                       class_name='Unnamed',
                                       class_name_plural='Unnamed Plural',
                                       total=20,
                                       workers_employed=0,
                                       gold_cost=65,
                                       wood_cost=20,
                                       stone_cost=0,
                                       output=1,
                                       description='Each {} adds +{} to your birth rate.'),
                     'field': Building(name='field',
                                       class_name='Unnamed',
                                       class_name_plural='Unnamed Plural',
                                       total=10,
                                       workers_employed=5,
                                       gold_cost=50,
                                       wood_cost=10,
                                       stone_cost=0,
                                       output=40,
                                       description='Each {} provides enough grain for {} people a day.'),
                     'pasture': Building(name='pasture',
                                         class_name='Unnamed',
                                         class_name_plural='Unnamed Plural',
                                         total=10,
                                         workers_employed=15,
                                         gold_cost=75,
                                         wood_cost=20,
                                         stone_cost=0,
                                         output=60,
                                         description='Each {} can feed {} people a day, but excess dairy is lost.'),
                     'mill': Building(name='mill',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=3,
                                      workers_employed=15,
                                      gold_cost=100,
                                      wood_cost=20,
                                      stone_cost=0,
                                      output=4,
                                      description='Each {} produces {} wood a day.'),
                     'mine': Building(name='mine',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=2,
                                      workers_employed=15,
                                      gold_cost=85,
                                      wood_cost=25,
                                      stone_cost=0,
                                      output=2,
                                      description='Each {} produces {} iron a day.'),
                     'quarry': Building(name='quarry',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=1,
                                        workers_employed=15,
                                        gold_cost=75,
                                        wood_cost=30,
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
                                      stone_cost=20,
                                      output=6,
                                      description='Each {} adds +{}% to your county\'s defence value.'),
                     'stables': Building(name='stables',
                                         class_name='Unnamed',
                                         class_name_plural='Unnamed Plural',
                                         total=0,
                                         workers_employed=15,
                                         gold_cost=80,
                                         wood_cost=20,
                                         stone_cost=5,
                                         output=5,
                                         description='Each {} lets your army return from battle {}% faster.'),
                     'bank': Building(name='bank',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=0,
                                      workers_employed=15,
                                      gold_cost=85,
                                      wood_cost=25,
                                      stone_cost=5,
                                      output=6,
                                      description="Each {} gives you {} additional gold per day."),
                     'tavern': Building(name='tavern',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=0,
                                        workers_employed=15,
                                        gold_cost=80,
                                        wood_cost=25,
                                        stone_cost=10,
                                        output=5,
                                        description="Each {} gives you {} additional spy to send on missions."),
                     'tower': Building(name='tower',
                                       class_name='watch tower',
                                       class_name_plural='watch towers',
                                       total=0,
                                       workers_employed=5,
                                       gold_cost=50,
                                       wood_cost=15,
                                       stone_cost=5,
                                       output=1,
                                       description="Each {} gives you +{}% defence against enemy thieves."),
                     'lab': Building(name='lab',
                                     class_name='Unnamed',
                                     class_name_plural='Unnamed Plural',
                                     total=0,
                                     workers_employed=15,
                                     gold_cost=105,
                                     wood_cost=20,
                                     stone_cost=10,
                                     output=4,
                                     description="Each {} generates {} research points per day."),
                     'arcane': Building(name='arcane',
                                        class_name='Unnamed',
                                        class_name_plural='Unnamed Plural',
                                        total=0,
                                        workers_employed=15,
                                        gold_cost=65,
                                        wood_cost=25,
                                        stone_cost=15,
                                        output=1,
                                        description="Each {} generates {} mana crystal each day."),
                     'lair': Building(name='lair',
                                      class_name='Unnamed',
                                      class_name_plural='Unnamed Plural',
                                      total=0,
                                      workers_employed=15,
                                      gold_cost=250,
                                      wood_cost=125,
                                      stone_cost=75,
                                      output=1,
                                      description="Each {} allows you to capture and train {} monster.")
                     }
