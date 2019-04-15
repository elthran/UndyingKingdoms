from undyingkingdoms.models.achievements import Achievement

# Current price balance: 1 stone == 2 iron == 2 mana == 4 wood == 4 research == 6 gold == 60 food


metadata_races = ['Human', 'Elf', 'Dwarf', 'Goblin']
metadata_titles = ['Sir', 'Dame', 'Lord', 'Lady', 'Baron', 'Baroness', 'Duke', 'Duchess', 'Prince', 'Princess']

metadata_backgrounds = ['Warlord', 'Engineer', 'Merchant', 'Rogue', 'Wizard']

kingdom_names = ["Faenoth", "Ecthalion"]

infiltration_missions = ['scout military', 'pilfer', 'burn crops', 'sow distrust', 'steal research']

attack_types = ["Attack", "Pillage", "Raze"]

tax_options = [(i, i) for i in range(16)]

rations_terminology = [(0, "None"), (0.25, "Quarter"), (0.5, "Half"), (0.75, "Three-Quarters"), (1, "Normal"), (1.5, "One-and-a-half"), (2, "Double"), (3, "Triple")]

excess_worker_choices = [(0, 'Produce Gold'), (1, 'Reclaim Land'), (2, 'Gather Food'), (3, 'Relax')]

all_buildings = ['house', 'field', 'pasture', 'mill', 'mine', 'quarry', 'fort', 'stables', 'tavern', 'tower', 'bank', 'lab', 'arcane', 'lair']

# Don't use modifier in name unless it is racial or class modifier dictionary.
land_to_clear_ratio = 5

all_achievements = {
    'land': Achievement(name="land", category="reach_x_amount_in_one_age", sub_category="land",
                        display_title="From Coast to Coast",
                        description="Have your county reach x amount of land in one playthrough.",
                        tier1=175, tier2=250, tier3=300, tier4=400, tier5=500, maximum_tier=5,
                        points_rewarded=5),
    'population': Achievement(name="population", category="reach_x_amount_in_one_age", sub_category="population",
                              display_title="Like Rabbits...",
                              description="Have your county reach x population in one playthrough.",
                              tier1=750, tier2=1500, tier3=2250, tier4=3000, tier5=4000, maximum_tier=5,
                              points_rewarded=5),
    'gold': Achievement(name="gold", category="reach_x_amount_in_one_age", sub_category="gold",
                        display_title="Midas Touch",
                        description="Have your county reach x gold in one playthrough.",
                        tier1=1000, tier2=2000, tier3=3000, tier4=4000, tier5=5000, maximum_tier=5,
                        points_rewarded=5),
    'wood': Achievement(name="wood", category="reach_x_amount_in_one_age", sub_category="wood",
                        display_title="Where Did the Forests Go?",
                        description="Have your county reach x wood in one playthrough.",
                        tier1=500, tier2=1000, tier3=1500, tier4=2000, tier5=2500, maximum_tier=5,
                        points_rewarded=5),
    'iron': Achievement(name="iron", category="reach_x_amount_in_one_age", sub_category="iron",
                        display_title="Heart of Iron",
                        description="Have your county reach x iron in one playthrough.",
                        tier1=500, tier2=1000, tier3=1500, tier4=2000, tier5=2500, maximum_tier=5,
                        points_rewarded=5),
    'stone': Achievement(name="stone", category="reach_x_amount_in_one_age", sub_category="stone",
                         display_title="Stone Cold",
                         description="Have your county reach x stone in one playthrough.",
                         tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
                         points_rewarded=5),
    'research': Achievement(name="research", category="reach_x_amount_in_one_age", sub_category="research",
                            display_title="Genius",
                            description="Have your county reach x research in one playthrough.",
                            tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
                            points_rewarded=5),
    'mana': Achievement(name="mana", category="reach_x_amount_in_one_age", sub_category="mana",
                        display_title="Wizard Master",
                        description="Have your county reach x mana in one playthrough.",
                        tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
                        points_rewarded=5),
    'dwarf_class_leader': Achievement(name="dwarf_class_leader", category="class_leader", sub_category="dwarf",
                                      display_title="Lord Under the Mountain!",
                                      description="Become the leader of your kingdom while playing as Dwarves.",
                                      maximum_tier=1,
                                      points_rewarded=15),
    'human_class_leader': Achievement(name="human_class_leader", category="class_leader", sub_category="human",
                                      display_title="Return of the King",
                                      description="Become the leader of your kingdom while playing as Humans.",
                                      maximum_tier=1,
                                      points_rewarded=15),
    'elf_class_leader': Achievement(name="elf_class_leader", category="class_leader", sub_category="elf",
                                    display_title="King of the Forest",
                                    description="Become the leader of your kingdom while playing as Elves.",
                                    maximum_tier=1,
                                    points_rewarded=15),
    'goblin_class_leader': Achievement(name="goblin_class_leader", category="class_leader", sub_category="goblin",
                                       display_title="The Goblin King",
                                       description="Become the leader of your kingdom while playing as Goblins.",
                                       maximum_tier=1,
                                       points_rewarded=15)
}

# Racial/Class Modifiers (A modifier of 0 means +0%. A modifier of 1 would mean +100%)
# Percents
birth_rate_modifier = {'Elf': ("Elders", -0.15), 'Goblin': ("Expendable", 0.15)}
death_rate_modifier = {}
income_modifier = {'Merchant': ("Silver Tongue", 0.15)}
offensive_power_modifier = {'Warlord': ("Relentless", 0.10)}
infiltration_success_modifier = {'Rogue': ("Master of Disguise", 10), 'Goblin': ("Sneaky", 10)}
production_per_worker_modifier = {'Dwarf': ("Dwarven Steel", 0.15), 'Engineer': ("Artisan", 0.20)}
defense_per_citizen_modifier = {'Elf': ("Citizen Militia", 1.00)}
food_consumed_modifier = {'Dwarf': ("Ravenous", 0.15)}
# Amounts
happiness_modifier = {'Goblin': ("Infighting", -1)}
buildings_built_per_day_modifier = {'Engineer': ("Craftsman", 1)}
amount_of_thieves_modifier = {'Rogue': ("Army of Shadows", 2)}
spell_chance_modifier = {'Wizard': ("Loremaster", 10), 'Elf': ("Affinity", 5)}


all_armies = ["peasant", "archer", "soldier", "elite", "monster"]

game_descriptions = {"attack": "How much power a unit has when attacking another county.",
                     "defence": "How much power a unit has when defending your county.",
                     "health": "Health affects how many of your units die in battle.",
                     "besieger_attack": "Each siege machine has attack equal to the number of fortifications in the defending county.",
                     "available_workers": "Any citizen not in the military or employed, is available. These workers "
                                          "will add production to your city which can be used to build new buildings. "
                                          "Unused production generates gold.",
                     "upkeep": "Monthly cost of paying your soldiers' salaries.",
                     "upkeep_daily": "Today's expected salary cost."}
