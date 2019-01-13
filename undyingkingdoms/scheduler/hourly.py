import sys

path = u'/home/undyingkingdoms/UndyingKingdoms/'
if path not in sys.path:
    sys.path = [path] + sys.path

import undyingkingdoms.models as models

# Advance the day
world = models.World.query.first()
world.advance_day()

