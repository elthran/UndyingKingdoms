def validate_targeting(county, spell, target):
    eligible_targets = [spell.targets]
    if eligible_targets[0] == 'friendly':
        eligible_targets.append('self')
    if county == target:
        target_relation = 'self'
    elif target.kingdom in county.kingdom.allies:
        target_relation = 'friendly'
    else:
        target_relation = 'hostile'

    invalid_target = (target_relation not in eligible_targets)
    return invalid_target, target_relation
