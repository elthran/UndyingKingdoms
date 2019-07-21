from random import randint


class Event:
    def __init__(self, county):
        self.county = county

    def build_random_daily_events(self, notifier):
        county = self.county
        infrastructure = county.infrastructure
        preferences = county.preferences
        preferences.days_since_event += 1
        random_chance = randint(0, preferences.days_since_event)
        if random_chance < 15:
            return
        random_chance = randint(1, 8)
        notification = None
        if random_chance == 1 and county.grain_stores > 0:
            amount = int(randint(3, 7) * county.grain_stores / 100)
            notification = notifier(
                county,
                "Rats have gotten into your grain silos",
                f"Your county lost {amount} of its stored grain.",
            )
            county.grain_stores -= amount

        elif random_chance == 2 and county.happiness > 90:
            amount = randint(100, 200)
            notification = notifier(
                county,
                "Your people celebrate your rule",
                f"Your people hold a feast and offer you {amount} gold as tribute.",
            )
            county.gold += amount

        elif random_chance == 3 and infrastructure.buildings['pasture'].total > 0:
            amount = min(randint(2, 4), infrastructure.buildings['pasture'].total)
            notification = notifier(
                county,
                "A disease has affected your cattle",
                f"Your county has lost {amount} of its dairy farms.",
            )
            infrastructure.buildings['pasture'].total -= amount

        elif random_chance == 4 and infrastructure.buildings['field'].total > 0:
            amount = min(randint(1, 3), infrastructure.buildings['field'].total)
            notification = notifier(
                county,
                "Storms have ravaged your crops",
                f"A massive storm has destroyed {amount} of your fields.",
            )
            infrastructure.buildings['field'].total -= amount
            preferences.weather = 'thunderstorm'

        elif random_chance == 5 and infrastructure.buildings['field'].total > 0:
            amount = infrastructure.buildings['field'].total * 15
            notification = notifier(
                county,
                "Booster crops",
                f"Due to excellent weather this season, your crops produced an addition {amount} grain today.",
            )
            county.grain_stores += amount
            preferences.weather = 'lovely'

        elif random_chance == 6:
            modifier = ((101 - county.healthiness) // 20 + 3) / 100  # Percent of people who will die (1% -> 5%)
            amount = int(modifier * county.population)
            notification = notifier(
                county,
                "Black Death",
                f"A plague has swept over our county, killing {amount} of our people.",
            )
            county.population -= amount

        elif random_chance == 7 and infrastructure.buildings['house'].total > 0:
            amount = min(randint(2, 4), infrastructure.buildings['house'].total)
            building_name = infrastructure.buildings['house'].class_name
            notification = notifier(
                county,
                "Disaster",
                f"A fire has spread in the city burning down {amount} of your {building_name}.",
            )
            infrastructure.buildings['house'].total -= amount
        if notification:
            notification.category = "Random Event"
            notification.save()
            preferences.days_since_event = 0
