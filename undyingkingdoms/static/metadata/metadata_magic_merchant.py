from undyingkingdoms.models.magic import Magic

merchant_spells = {
    'steal_gold': Magic(name='steal_gold',
                        display_name='Golden Tongue',
                        source='Merchant',
                        category='instant',
                        targets='hostile',
                        known=True,
                        mana_cost=15,
                        output=150,
                        description='Immediately convince an enemy county to give you gold.'),
    'instant_happiness': Magic(
        name='instant_happiness',
        display_name='Charisma',
        category='instant',
        targets='self',
        known=True,
        mana_cost=10,
        output=5,
        description='Adds +5 happiness to your county.'
    )
}
