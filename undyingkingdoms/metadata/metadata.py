# Current price balance: 1 stone == 2 iron == 2 mana == 4 wood == 4 research == 6 gold == 60 food


metadata_races = ['Dwarf', 'Elf', 'Goblin', 'Human', 'Ogre']
metadata_titles = ['Sir', 'Dame', 'Lord', 'Lady', 'Baron', 'Baroness', 'Duke', 'Duchess', 'Prince', 'Princess']

metadata_backgrounds = ['Alchemist', 'Artificer', 'Cleric', 'Diplomat', 'Druid',
                        'Hierophant', 'Merchant', 'Rogue', 'Warlord', 'Wizard']
metadata_background_descriptions = {
    'Alchemist': 'Specializes in hastening research and converting resources.',
    'Artificer': 'An expert in engineering and infrastructure.',
    'Cleric': 'Has access to many blessings and wards of protection for your county.',
    'Diplomat': 'Has the ability to persuade other counties.',
    'Druid': 'An affinity with nature allows them to master food production.',
    'Hierophant': 'A master cultist who can cast powerful rituals through sacrificing their people.',
    'Merchant': 'A master of bartering and economics.',
    'Rogue': 'Capable of espionage and assassination.',
    'Warlord': 'A master tactician, capable of dominating the battlefield.',
    'Wizard': 'Has access to a wide arsenal of powerful magic.'}

# Warlord: <Battle> and combat.
# Wizard: <Magic> and casting and summons
# Rogue: <Thieving> and betrayal and assassinations
# Druid: <Food> and nature and healing
# Cleric: <Health> and happiness
# Alchemist: <Science/Tech> and resource conversion
# Merchant: <Economy> and happiness and persuasion
# Artificer: <Infrastructure>
# Diplomat: <Diplomacy>
# Hierophant: <Sacrifice> and rituals

kingdom_names = ["Faenoth", "Ecthalion"]

infiltration_missions = ['scout military', 'pilfer', 'burn crops', 'sow distrust', 'steal research']

attack_types = ["Attack", "Pillage", "Raze"]

tax_options = [(i, i) for i in range(16)]

rations_terminology = [(0, "None"), (0.25, "Quarter"), (0.5, "Half"), (0.75, "Three-Quarters"), (1, "Normal"),
                       (1.5, "One-and-a-half"), (2, "Double"), (3, "Triple")]

excess_worker_choices = [(0, 'Produce Gold'), (1, 'Reclaim Land'), (2, 'Gather Food'), (3, 'Relax')]

all_buildings = ['house', 'field', 'pasture', 'mill', 'mine', 'quarry', 'fort', 'stables', 'tavern', 'tower', 'bank',
                 'lab', 'arcane', 'lair']

# Don't use modifier in name unless it is racial or class modifier dictionary.
land_to_clear_ratio = 5

# Racial/Class Modifiers (A modifier of 0 means +0%. A modifier of 1 would mean +100%)
# Percents
birth_rate_modifier = {'Elf': ("Elders", -0.15), 'Goblin': ("Expendable", 0.15), 'Ogre': ("Solitary", -0.25)}
death_rate_modifier = {}
income_modifier = {'Merchant': ("Silver Tongue", 0.15)}
offensive_power_modifier = {'Warlord': ("Relentless", 0.10)}
infiltration_results_modifier = {'Rogue': ("Master of Disguise", 0.15), 'Ogre': ("Simple-minded", -0.10),
                                 'Goblin': ("Sneaky", 0.10)}
production_per_worker_modifier = {'Dwarf': ("Dwarven Steel", 0.15)}
defense_per_citizen_modifier = {'Elf': ("Citizen Militia", 1.00)}
food_consumed_modifier = {'Dwarf': ("Ravenous", 0.15), 'Ogre': ("Gigantic", 0.20)}
food_produced_modifier = {'Druid': ("Naturalist", 0.10)}
# Amounts
happiness_modifier = {'Goblin': ("Infighting", -1)}
amount_of_thieves_modifier = {'Rogue': ("Army of Shadows", 2)}
spell_results_modifier = {'Wizard': ("Loremaster", 10), 'Elf': ("Affinity", 5)}
buildings_produced_per_day = {'Artificer': ("Engineer", 1)}

all_armies = ["peasant", "archer", "soldier", "besieger", "summon", "elite", "monster"]

game_descriptions = {"attack": "How much power a unit has when attacking another county.",
                     "defence": "How much power a unit has when defending your county.",
                     "health": "Health affects how many of your units die in battle.",
                     "besieger_attack": "Each siege machine has attack equal to the number of fortifications in the defending county.",
                     "available_workers": "Any citizen not in the military or employed, is available. These workers "
                                          "will add production to your city which can be used to build new buildings. "
                                          "Unused production generates gold.",
                     "upkeep": "Monthly cost of paying your soldiers' salaries.",
                     "upkeep_daily": "Today's expected salary cost."}
