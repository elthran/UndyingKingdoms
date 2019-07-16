from app.models.magic import Magic

dwarf_spells = {
    'population_killer': Magic(name='population_killer',
                               display_name='Rune Lightning',
                               source='Dwarf',
                               category='instant',
                               targets='hostile',
                               known=True,
                               mana_cost=15,
                               output=4,
                               description='A blasts of lightning hits the enemy county, '
                                           'killing 4% of their populace.'),
    'convert_iron_to_gold': Magic(name='convert_iron_to_gold',
                                  display_name='Rune of Alchemy',
                                  source='Dwarf',
                                  category='instant',
                                  targets='self',
                                  known=True,
                                  mana_cost=5,
                                  output=10,
                                  description='Instantly turns 10 iron into 100 gold.'),
    'modify_magic_disrupt': Magic(
        name='modify_magic_disrupt',
        display_name='Rune of Shielding',
        source='Dwarf',
        category='aura',
        targets='self',
        known=True,
        mana_cost=10,
        mana_sustain=2,
        output=30,
        description='While active, '
                    'you have a +30% chance of disrupting enemy spells.')
}
