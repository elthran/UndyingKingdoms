from app.models.buildings import Building

generic_buildings = {
    'house': Building(
        name='house',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=20,
        workers_employed=0,
        gold_cost=65,
        wood_cost=20,
        stone_cost=0,
        output=5,
        description='Each percent of land built as a {0} increases your birth rate.'
    ),
    'field': Building(
        name='field',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=10,
        workers_employed=5,
        gold_cost=50,
        wood_cost=10,
        stone_cost=0,
        output=40,
        description='Each {0} provides enough grain to feed {1} people a day.'
    ),
    'pasture': Building(
        name='pasture',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=10,
        workers_employed=15,
        gold_cost=75,
        wood_cost=20,
        stone_cost=0,
        output=60,
        description='Each {0} produces enough dairy to feed {1} people a day, '
                    'but excess dairy is lost.'
    ),
    'mill': Building(
        name='mill',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=3,
        workers_employed=10,
        gold_cost=100,
        wood_cost=20,
        stone_cost=0,
        output=4,
        description='Each {0} produces {1} wood a day.'
    ),
    'mine': Building(
        name='mine',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=2,
        workers_employed=10,
        gold_cost=85,
        wood_cost=25,
        stone_cost=0,
        output=2,
        description='Each {0} produces {1} iron a day.'
    ),
    'quarry': Building(
        name='quarry',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=1,
        workers_employed=10,
        gold_cost=75,
        wood_cost=30,
        stone_cost=0,
        output=1,
        description='Each {0} produces {1} stone a day.'
    ),
    'fort': Building(
        name='fort',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=25,
        gold_cost=100,
        wood_cost=75,
        stone_cost=20,
        output=8,
        description='Each {0} adds +{1}% to your county\'s defence value, '
                    'but are vulnerable to siege weapons.'
    ),
    'stables': Building(
        name='stables',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=15,
        gold_cost=80,
        wood_cost=20,
        stone_cost=5,
        output=10,
        description='Each percent of land built as {0} helps your army return from battle faster.'
    ),
    'bank': Building(
        name='bank',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=10,
        gold_cost=85,
        wood_cost=25,
        stone_cost=5,
        output=6,
        description="Each {0} produces {1} additional gold per day."
    ),
    'tavern': Building(
        name='tavern',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=10,
        gold_cost=80,
        wood_cost=25,
        stone_cost=10,
        output=1,
        description="Each {0} gives you {1} additional spy to send on missions."
    ),
    'tower': Building(
        name='tower',
        class_name='watch tower',
        class_name_plural='watch towers',
        total=0,
        workers_employed=5,
        gold_cost=50,
        wood_cost=15,
        stone_cost=5,
        output=7,
        description="Each percent of land dedicated to {0} gives you a better chance to catch enemy thieves."
    ),
    'lab': Building(
        name='lab',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=10,
        gold_cost=105,
        wood_cost=20,
        stone_cost=10,
        output=4,
        description="Generates {1} points of research each day."
    ),
    'arcane': Building(
        name='arcane',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=10,
        gold_cost=65,
        wood_cost=25,
        stone_cost=15,
        output=5,
        description="Increases effectiveness of spells by {1}% for each {0}."
    ),
    'lair': Building(
        name='lair',
        class_name='Unnamed',
        class_name_plural='Unnamed Plural',
        total=0,
        workers_employed=10,
        gold_cost=250,
        wood_cost=125,
        stone_cost=75,
        output=1,
        description="Each {0} allows you to capture and train {1} monster."
    )
}
