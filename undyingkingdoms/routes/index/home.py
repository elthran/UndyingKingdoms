from flask import url_for, redirect
from undyingkingdoms import app, db

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))
