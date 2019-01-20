from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    title = StringField('Title',
                        validators=[Length(min=0, max=32)])
    content = StringField('Content',
                          validators=[DataRequired(message='Your post requires a message.'), Length(min=0, max=5000)])

