def max_buildable_by_cost(county, building):
    max_size = min(
        county.gold // building.gold_cost,
        county.wood // building.wood_cost,
        (county.stone // building.stone_cost
            if building.stone_cost
            else float('inf')),
        # eventually the 1 will be a land cost.
        county.get_available_land() // 1,
        (county.get_available_workers() // building.workers_employed
            if building.workers_employed
            else float('inf'))
    )
    return max_size
