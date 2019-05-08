from ..technologies import Technology
from .counties import County
from .economy import Economy

from .economy_addon import economy_addon
from .tech_addon import tech_addon
from .casting_addon import casting_addon

# Attach any add-ons needed to the County class.
casting_addon(County)
tech_addon(County, Technology)
economy_addon(County, Economy)
