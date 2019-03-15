from undyingkingdoms.models.armies import Army

generic_armies = {'peasant': Army(name='peasant',
                                  class_name='peasant',
                                  class_name_plural='peasants',
                                  total=0,
                                  trainable_per_day=25,
                                  gold=7,
                                  iron=2,
                                  wood=1,
                                  upkeep=10,
                                  attack=2,
                                  defence=1,
                                  health=1,
                                  description='Unknown'),
                  'soldier': Army(name='soldier',
                                  class_name='soldier',
                                  class_name_plural='soldiers',
                                  total=0,
                                  trainable_per_day=15,
                                  gold=15,
                                  iron=5,
                                  wood=3,
                                  upkeep=25,
                                  attack=7,
                                  defence=1,
                                  health=3,
                                  description='Unknown'),
                  'archer': Army(name='archer',
                                 class_name='archer',
                                 class_name_plural='archers',
                                 total=20,
                                 trainable_per_day=10,
                                 gold=22,
                                 iron=6,
                                 wood=4,
                                 upkeep=30,
                                 attack=0,
                                 defence=5,
                                 health=4,
                                 description='Unknown'),
                  'elite': Army(name='elite',
                                class_name='elite',
                                class_name_plural='elites',
                                total=0,
                                trainable_per_day=5,
                                gold=33,
                                iron=10,
                                wood=6,
                                upkeep=50,
                                attack=12,
                                defence=5,
                                health=6,
                                description='Unknown'),
                  'monster': Army(name='monster',
                                  class_name='monster',
                                  class_name_plural='monsters',
                                  total=0,
                                  trainable_per_day=1,
                                  gold=125,
                                  iron=40,
                                  wood=20,
                                  upkeep=200,
                                  attack=50,
                                  defence=30,
                                  health=25,
                                  description='Unknown')
                  }
