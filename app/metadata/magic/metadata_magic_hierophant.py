from app.models.magic import Magic

hierophant_spells = {
    'convert_iron_to_gold': Magic(name='convert_iron_to_gold',
                                  display_name='Secrets of Alchemy',
                                  source='Hierophant',
                                  category='instant',
                                  targets='self',
                                  known=True,
                                  mana_cost=10,
                                  output=20,
                                  description='Instantly turns 10 iron into 200 gold.'),
    'instant_research': Magic(name='instant_research',
                              display_name='Hidden Knowledge',
                              source='Hierophant',
                              category='instant',
                              targets='self',
                              known=True,
                              mana_cost=25,
                              output=50,
                              description='Instantly learn 50 research towards your current technology.'),
    'summon_tier_1': Magic(
        name='summon_tier_1',
        display_name='Summon Lesser Daemon',
        source='Hierophant',
        category='instant',
        targets='self',
        known=True,
        mana_cost=5,
        output=1,
        description='Summon a Lesser Daemon to join your army.'
    )
}
