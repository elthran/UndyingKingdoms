from undyingkingdoms.models.magic import Magic

dwarf_spells = {'population_killer_tier_1': Magic(name='population_killer_tier_1',
                                                  display_name='rune lightning',
                                                  category='instant',
                                                  targets='hostile',
                                                  known=True,
                                                  mana_cost=15,
                                                  output=5,
                                                  description='A blasts of lightning hits the enemy county, killing 5% of their populace.'),
                'secrets of alchemy': Magic(name='secrets of alchemy',
                                            display_name='alchemy',
                                            category='instant',
                                            targets='self',
                                            known=True,
                                            mana_cost=5,
                                            description='Immediately turns 10 iron into 100 gold.')
                }

# Escape from the maze by moving to the X mark.
# Try to collect as many coins as you can.
hero.attack("Treasure Chest")
hero.attack("Treasure Chest")


def rightUp():
    hero.moveRight()
    hero.moveUp()


hero.moveUp()
hero.moveUp()
hero.moveUp()
hero.moveUp()
hero.moveDown()

enemy = hero.findNearestEnemy()
while enemy.health > 0:
    hero.attack(enemy)
hero.moveRight()
hero.moveRight()
hero.moveLeft()
hero.moveLeft()
hero.moveDown()
hero.moveDown()
hero.moveDown()
hero.moveDown()
hero.moveRight()
rightUp()
hero.moveLeft()
enemy = hero.findNearestEnemy()
while enemy.health > 0:
    hero.attack(enemy)
hero.moveUp()
hero.moveUp()
hero.moveDown()
hero.moveDown()
hero.moveRight()
rightUp()
rightUp()

hero.moveLeft()
enemy = hero.findNearestEnemy()
while enemy.health > 0:
    hero.attack(enemy)
hero.moveUp()
hero.moveUp()
hero.moveDown()
hero.moveDown()

hero.moveRight()
rightUp()
rightUp()

hero.moveLeft()
enemy = hero.findNearestEnemy()
while enemy.health > 0:
    hero.attack(enemy)
hero.moveUp()
hero.moveUp()
hero.moveDown()
hero.moveDown()

hero.moveRight()
rightUp()

rightUp()
