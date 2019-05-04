from undyingkingdoms.models.magic import Magic

ogre_spells = {
    'population_killer': Magic(name='population_killer',
                               display_name='Death Ritual',
                               source='Ogre',
                               category='instant',
                               targets='hostile',
                               known=True,
                               mana_cost=12,
                               output=5,
                               description='An unholy magic kills 5% of their population.'),
    'modify_offensive_power': Magic(name='modify_offensive_power',
                                    display_name='Ritual of Blood',
                                    source='Ogre',
                                    category='aura',
                                    targets='self',
                                    known=True,
                                    mana_cost=20,
                                    mana_sustain=3,
                                    output=0.25,
                                    description='Increases your offensive military power by 25%.'),
    'modify_magic_disrupt': Magic(
        name='modify_magic_disrupt',
        display_name='Shield of Gorgrath',
        source='Ogre',
        category='aura',
        targets='self',
        known=True,
        mana_cost=15,
        mana_sustain=2,
        output=35,
        description='While active, '
                    'you have a +35% chance of disrupting enemy spells.')
}
