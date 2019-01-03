from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ForumPost(FlaskForm):
    title = StringField('Title', [DataRequired(message='Your post requires a title.')])
    message = StringField('Message', [DataRequired(message='You must enter a message.')])

