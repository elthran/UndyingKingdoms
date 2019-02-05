from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    TITLE_SIZE = 32
    CONTENT_SIZE = 5000
    title = StringField('Title', validators=[Length(min=0, max=TITLE_SIZE)])
    content = StringField('Content', validators=[DataRequired(message='Your post requires a message.'), Length(min=0, max=CONTENT_SIZE)])

