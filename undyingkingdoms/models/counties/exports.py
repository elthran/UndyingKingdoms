from .counties import County
from ..technologies import Technology
from .economy import Economy
from .infrastructure import Infrastructure
from .espionage import Espionage
from .military import Military
from .wizardry import Wizardry
from .scientist import Scientist

from .sub_table_addon import sub_table_addon
from .tech_addon import tech_addon
from .casting_addon import casting_addon

# Attach any add-ons needed to the County class.
casting_addon(County)
tech_addon(County, Technology)
sub_table_addon(County, Economy)
sub_table_addon(County, Military, hoist=False)
sub_table_addon(County, Wizardry)
sub_table_addon(County, Scientist)
sub_table_addon(County, Espionage)
sub_table_addon(County, Infrastructure)
