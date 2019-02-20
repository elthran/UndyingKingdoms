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
@mobile_template('{mobile/}index/initialize.html')
def initialize(template):
    if current_user.county is not None:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    titles = ["<Title>"] + metadata_titles
    players_titles = min((current_user.alpha_wins * 2) + 3, len(titles))
    races = ["<Race>"] + metadata_races
    backgrounds = ["<Class>"] + metadata_backgrounds
    form = InitializeForm()
    form.title.choices = [(i, titles[i]) for i in range(players_titles)]
    form.race.choices = [(i, races[i]) for i in range(len(races))]
    form.background.choices = [(i, backgrounds[i]) for i in range(len(backgrounds))]
    
    kingdoms = Kingdom.query.all()
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
    
    if form.validate_on_submit():
        county = County(smallest_kingdom.id,
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
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    return render_template(template, form=form,
                           dwarf_armies=dwarf_armies,
                           human_armies=human_armies,
                           elf_armies=elf_armies,
                           goblin_armies=goblin_armies)
