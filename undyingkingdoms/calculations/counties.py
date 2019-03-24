from random import uniform


def get_attack_power(county_id, army):
    """Returns the attack power of your army"""
    strength = 0
    county = County.query.get(county_id)
    for name, amount in army.items():
        strength += county.armies.values()[name].attack * amount
    strength *= uniform(0.85, 1.15)
    return int(strength)
