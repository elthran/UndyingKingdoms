from flask import url_for, redirect, render_template
from flask_login import current_user, login_required

from undyingkingdoms import app
from undyingkingdoms.controler.initialize import initialize_county, pick_kingdom
from undyingkingdoms.models.forms.initialize import InitializeForm
from undyingkingdoms.static.metadata.metadata import metadata_races, metadata_backgrounds, metadata_titles
from undyingkingdoms.static.metadata.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.metadata_armies_human import human_armies


@app.route('/initialize/', methods=['GET', 'POST'])
@login_required
def initialize():
    if not current_user.is_verified:
        return redirect(url_for('activate'))
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

    if form.validate_on_submit():
        has_clan = form.data.clan == 1
        kingdom = pick_kingdom(current_user, has_clan)

        race = races[form.data.race]
        title = titles[form.title.data]
        background = backgrounds[form.background.data]
        county_name = form.county.data
        leader_name = form.leader.data
        initialize_county(
            current_user, kingdom, county_name, leader_name, background, race, title
        )
        return redirect(url_for('overview'))
    return render_template(
        "index/initialize.html",
        form=form,
        dwarf_armies=dwarf_armies,
        human_armies=human_armies,
        elf_armies=elf_armies,
        goblin_armies=goblin_armies
    )
