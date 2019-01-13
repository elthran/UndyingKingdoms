from undyingkingdoms.models import World

# Advance the day
world = World.query.first()
world.advance_day()

