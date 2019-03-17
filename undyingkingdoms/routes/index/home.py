from flask import url_for, redirect, render_template
from undyingkingdoms import app, db


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))


@app.route('/m', defaults={'path': ''})
@app.route('/m/<path:path>')
def mobile(path):
    return render_template('dist/index.html')
