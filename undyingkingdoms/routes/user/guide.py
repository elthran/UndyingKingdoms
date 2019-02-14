import pandas as pd

from flask import render_template
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app


@app.route('/user/guide/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/guide.html')
@login_required
def guide(template):

    # these should get generated here too ...
    races = pd.read_excel('undyingkingdoms/static/metadata/modifiers.xlsx', sheet_name='Modifiers', index_col=0)
    armies = pd.read_excel('undyingkingdoms/static/metadata/armies.xlsx', sheet_name='Armies', index_col=0)
    return render_template(template, races=races, armies=armies)
