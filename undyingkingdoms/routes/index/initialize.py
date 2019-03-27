from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom
from undyingkingdoms.models.forms.initialize import InitializeForm
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_backgrounds, metadata_titles
from undyingkingdoms.static.metadata.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.metadata_armies_human import human_armies


@app.route('/initialize/', methods=['GET', 'POST'])
def initialize():
    if current_user.county is not None:
        return redirect(url_for('overview'))
    titles = ["<Title>"] + metadata_titles
    players_titles = min(7, len(titles))
    races = ["<Race>"] + metadata_races
    backgrounds = ["<Class>"] + metadata_backgrounds
    form = InitializeForm()
    form.title.choices = [(i, titles[i]) for i in range(players_titles)]
    form.race.choices = [(i, races[i]) for i in range(len(races))]
    form.background.choices = [(i, backgrounds[i]) for i in range(len(backgrounds))]
    if current_user.clan:
        form.clan.choices = [(i[0], i[1]) for i in [(0, "Random"), (1, "Clan")]]
    else:
        form.clan.choices = [(i[0], i[1]) for i in [(0, "Random")]]
    kingdoms = Kingdom.query.filter_by(clan=False).all()  # Select all public kingdoms
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))  # Get the smallest
    kingdom_id = smallest_kingdom.id
    
    if form.validate_on_submit():
        if form.clan.data == 1:
            kingdom_id = current_user.clan.kingdom_id
        county = County(kingdom_id,
                        form.county.data,
                        form.leader.data,
                        current_user.id,
                        races[form.race.data],
                        titles[form.title.data],
                        backgrounds[form.background.data])
        county.save()
        county.vote = county.id
        preferences = Preferences(county.id, county.user.id)
        preferences.save()
        return redirect(url_for('overview'))
    return render_template(
        "index/initialize.html",
        form=form,
        dwarf_armies=dwarf_armies,
        human_armies=human_armies,
        elf_armies=elf_armies,
        goblin_armies=goblin_armies
    )
