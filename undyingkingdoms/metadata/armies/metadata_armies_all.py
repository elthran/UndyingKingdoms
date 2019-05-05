from undyingkingdoms.models.armies import Army

generic_armies = {'peasant': Army(name='peasant',
                                  class_name='peasant',
                                  class_name_plural='peasants',
                                  total=0,
                                  trainable_per_day=20,
                                  gold=6,
                                  iron=2,
                                  wood=1,
                                  upkeep=8,
                                  category='Not Implemented',
                                  attack=2,
                                  defence=1,
                                  health=1,
                                  armour_type='Not Implemented',
                                  description='Unknown'),
                  'soldier': Army(name='soldier',
                                  class_name='soldier',
                                  class_name_plural='soldiers',
                                  total=0,
                                  trainable_per_day=10,
                                  gold=20,
                                  iron=4,
                                  wood=3,
                                  upkeep=25,
                                  category='Not Implemented',
                                  attack=6,
                                  defence=1,
                                  health=3,
                                  armour_type='Not Implemented',
                                  description='Unknown'),
                  'archer': Army(name='archer',
                                 class_name='archer',
                                 class_name_plural='archers',
                                 total=20,
                                 trainable_per_day=10,
                                 gold=25,
                                 iron=6,
                                 wood=4,
                                 upkeep=25,
                                 category='Not Implemented',
                                 attack=0,
                                 defence=5,
                                 health=4,
                                 armour_type='Not Implemented',
                                 description='Unknown'),
                  'besieger': Army(name='besieger',
                                   class_name='besieger',
                                   class_name_plural='besiegers',
                                   total=0,
                                   trainable_per_day=3,
                                   gold=50,
                                   iron=25,
                                   wood=25,
                                   upkeep=25,
                                   category='Infantry',
                                   attack=0,
                                   defence=0,
                                   health=10,
                                   armour_type='Not Implemented',
                                   description='Each {} has attack equal to the number of forts that the enemy has.'),
                  'elite': Army(name='elite',
                                class_name='elite',
                                class_name_plural='elites',
                                total=0,
                                trainable_per_day=5,
                                gold=40,
                                iron=10,
                                wood=6,
                                upkeep=50,
                                category='Infantry',
                                attack=12,
                                defence=2,
                                health=6,
                                armour_type='Not Implemented',
                                description='Unknown'),
                  'monster': Army(name='monster',
                                  class_name='monster',
                                  class_name_plural='monsters',
                                  total=0,
                                  trainable_per_day=1,
                                  gold=150,
                                  iron=50,
                                  wood=10,
                                  upkeep=200,
                                  category='Not Implemented',
                                  attack=50,
                                  defence=10,
                                  health=25,
                                  armour_type='Not Implemented',
                                  description='Unknown')
                  }