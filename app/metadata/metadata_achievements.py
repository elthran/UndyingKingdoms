from app.models.achievements import Achievement

all_achievements = [
    Achievement(
        name="land", category="reach_x_amount_in_one_age", sub_category="land",
        display_title="From Coast to Coast",
        description="Have your county reach x amount of land in one playthrough.",
        tier1=175, tier2=250, tier3=300, tier4=400, tier5=500, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="population", category="reach_x_amount_in_one_age", sub_category="population",
        display_title="Like Rabbits...",
        description="Have your county reach x population in one playthrough.",
        tier1=750, tier2=1500, tier3=2250, tier4=3000, tier5=4000, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="gold", category="reach_x_amount_in_one_age", sub_category="gold",
        display_title="Midas Touch",
        description="Have your county reach x gold in one playthrough.",
        tier1=1000, tier2=2000, tier3=3000, tier4=4000, tier5=5000, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="wood", category="reach_x_amount_in_one_age", sub_category="wood",
        display_title="Where Did the Forests Go?",
        description="Have your county reach x wood in one playthrough.",
        tier1=500, tier2=1000, tier3=1500, tier4=2000, tier5=2500, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="iron", category="reach_x_amount_in_one_age", sub_category="iron",
        display_title="Heart of Iron",
        description="Have your county reach x iron in one playthrough.",
        tier1=500, tier2=1000, tier3=1500, tier4=2000, tier5=2500, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="stone", category="reach_x_amount_in_one_age", sub_category="stone",
        display_title="Stone Cold",
        description="Have your county reach x stone in one playthrough.",
        tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="research", category="reach_x_amount_in_one_age", sub_category="research",
        display_title="Genius",
        description="Have your county reach x research in one playthrough.",
        tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="mana", category="reach_x_amount_in_one_age", sub_category="mana",
        display_title="Wizard Master",
        description="Have your county reach x mana in one playthrough.",
        tier1=250, tier2=500, tier3=1000, tier4=1500, tier5=2000, maximum_tier=5,
        points_rewarded=5
    ),
    Achievement(
        name="dwarf_class_leader", category="class_leader", sub_category="dwarf",
        display_title="Lord Under the Mountain!",
        description="Become the leader of your kingdom while playing as Dwarves.",
        maximum_tier=1,
        points_rewarded=15
    ),
    Achievement(
        name="human_class_leader", category="class_leader", sub_category="human",
        display_title="Return of the King",
        description="Become the leader of your kingdom while playing as Humans.",
        maximum_tier=1,
        points_rewarded=15
    ),
    Achievement(
        name="elf_class_leader", category="class_leader", sub_category="elf",
        display_title="King of the Forest",
        description="Become the leader of your kingdom while playing as Elves.",
        maximum_tier=1,
        points_rewarded=15
    ),
    Achievement(
        name="goblin_class_leader", category="class_leader", sub_category="goblin",
        display_title="The Goblin King",
        description="Become the leader of your kingdom while playing as Goblins.",
        maximum_tier=1,
        points_rewarded=15
    ),
]

all_achievements = {
    achievement.name: achievement
    for achievement in all_achievements
}
