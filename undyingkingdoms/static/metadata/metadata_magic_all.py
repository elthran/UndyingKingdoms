from undyingkingdoms.models.spells import Spell

generic_spells = {'peasant': Spell(name='peasant',
                                  class_name='peasant',
                                  class_name_plural='peasants',
                                  total=25,
                                  trainable_per_day=25,
                                  gold=5,
                                  iron=2,
                                  wood=1,
                                  upkeep=5,
                                  attack=1,
                                  defence=1,
                                  health=1,
                                  description='Unknown')
                  }
