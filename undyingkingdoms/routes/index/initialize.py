from flask import url_for, redirect, render_template
from flask_login import current_user

from undyingkingdoms import app
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.initialize import InitializeForm
from undyingkingdoms.static.metadata import dwarf_armies, human_armies


@app.route('/initialize/', methods=['GET', 'POST'])
def initialize():
    genders = ["----", "Female", "Male"]
    races = ["----", "Dwarf", "Human", "Elf"]
    form = InitializeForm()
    form.gender.choices = [(i, genders[i]) for i in range(len(genders))]
    form.race.choices = [(i, races[i]) for i in range(len(races))]
    if form.validate_on_submit():
        county = County(form.county.data,
                        form.leader.data,
                        current_user.id,
                        races[form.race.data],
                        genders[form.gender.data])
        county.save()
        county.vote = county.id
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    return render_template("index/initialize.html", form=form, dwarf_armies=dwarf_armies, human_armies=human_armies)
