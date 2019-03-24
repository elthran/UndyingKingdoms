from undyingkingdoms.models.magic import Magic

human_spells = {'meteor': Magic(name='meteor',
                              category='self',
                              targets='hostile',
                              known=True,
                              mana_cost=15,
                              description='A meteor blasts the enemy county, killing a chunk of their populace.')}
