from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    message = StringField('Message', [DataRequired(message='You must enter a message.')])

