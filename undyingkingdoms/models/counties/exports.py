from .military import Military
from ..technologies import Technology
from .counties import County
from .economy import Economy

from .sub_table_addon import sub_table_addon
from .tech_addon import tech_addon
from .casting_addon import casting_addon

# Attach any add-ons needed to the County class.
casting_addon(County)
tech_addon(County, Technology)
sub_table_addon(County, Economy)
sub_table_addon(County, Military)
