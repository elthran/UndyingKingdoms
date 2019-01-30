from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom
from undyingkingdoms.models.forms.initialize import InitializeForm
from undyingkingdoms.static.metadata import dwarf_armies, human_armies, elf_armies


@app.route('/initialize/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/initialize.html')
def initialize(template):
    if current_user.county is not None:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    genders = ["<Gender>", "Female", "Male"]
    races = ["<Race>", "Dwarf", "Human", "Elf"]
    titles = ["<Class>", "Warlord", "Engineer", "Merchant", "Rogue"]
    form = InitializeForm()
    form.gender.choices = [(i, genders[i]) for i in range(len(genders))]
    form.race.choices = [(i, races[i]) for i in range(len(races))]
    form.title.choices = [(i, titles[i]) for i in range(len(titles))]
    
    kingdoms = Kingdom.query.all()
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))
    
    if form.validate_on_submit():
        county = County(smallest_kingdom.id,
                        form.county.data,
                        form.leader.data,
                        current_user.id,
                        races[form.race.data],
                        genders[form.gender.data],
                        titles[form.title.data])
        county.save()
        county.vote = county.id
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    return render_template(template, form=form,
                           dwarf_armies=dwarf_armies,
                           human_armies=human_armies,
                           elf_armies=elf_armies)
