import pandas as pd

from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from app import app


@app.route('/user/guide/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/guide.html')
@login_required
def guide(template):

    races = None
    armies = None
    try:
        races = pd.read_csv('app/static/dist/modifiers.csv', index_col=0)
        armies = pd.read_csv('app/static/dist/armies.csv', index_col=0)
    except Exception as ex:
        app.logger.error("The guide comparision tables are failing: " + str(ex))
    return render_template(template, races=races, armies=armies)
