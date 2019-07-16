from random import uniform


def get_attack_power(county, army):
    """Returns the attack power of your army"""
    strength = 0
    for name, amount in army.items():
        strength += county.armies.values()[name].attack * amount
    strength *= uniform(0.85, 1.15)
    return int(strength)
