from flask import url_for, redirect, render_template
from flask_login import current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.initialize import InitializeForm


@app.route('/initialize/', methods=['GET', 'POST'])
def initialize():
    genders = ["----", "Female", "Male"]
    races = ["----", "Dwarf", "Human"]
    form = InitializeForm()
    form.gender.choices = [(i, genders[i]) for i in range(len(genders))]
    form.race.choices = [(i, races[i]) for i in range(len(races))]
    if form.validate_on_submit():
        print("CREATING", form.county.data,
              form.leader.data,
              current_user.id,
              1,
              races[form.race.data],
              genders[form.gender.data])
        county = County(form.county.data,
                        form.leader.data,
                        current_user.id,
                        1,
                        races[form.race.data],
                        genders[form.gender.data])
        print("ADDING")
        db.session.add(county)
        print("ADDED")
        db.session.commit()
        county.vote = county.id
        db.session.commit()
        return redirect(url_for('overview'))
    return render_template("index/initialize.html", form=form)
