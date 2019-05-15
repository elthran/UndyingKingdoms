from copy import deepcopy

from undyingkingdoms.metadata.research.metadata_research_dwarf import dwarf_technology
from undyingkingdoms.models.counties.counties import County


def test_set_unit_attribute(ctx):
    county = County.query.get(1)

    county.technologies.update(deepcopy(dwarf_technology))

    archer_defence = county.armies['archer'].defence

    county.technologies['dwarven muskets'].completed = True

    assert county.military.archer_defence > 0
    assert county.armies['archer'].defence > archer_defence

    county.technologies['dwarven muskets'].completed = False

    assert county.armies['archer'].defence == archer_defence
