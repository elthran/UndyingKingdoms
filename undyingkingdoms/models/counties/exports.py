from .tech_addons import completed_techs_addon, incomplete_techs_addon, \
    available_techs_addon, unavailable_techs_addon
from .casting_addon import casting_addon
from .counties import County

# Attach any add-ons needed to the County class.
casting_addon(County)
completed_techs_addon(County)
incomplete_techs_addon(County)
available_techs_addon(County)
unavailable_techs_addon(County)
