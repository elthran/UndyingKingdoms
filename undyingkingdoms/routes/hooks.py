from flask import render_template

from sqlalchemy.exc import DatabaseError

from undyingkingdoms import app, db


# Thanks to https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html
@app.after_request
def session_commit(response):
    if response.status_code >= 400:
        # I'm not sure if this is correct?
        # Maybe should redirect to 404?
        return response
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise
    # session.remove() is called for you by flask-sqlalchemy
    return response
