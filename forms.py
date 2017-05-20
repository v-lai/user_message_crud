from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    first_name = StringField('First name', [validators.Length(min=2)])
    last_name = StringField('Last name', [validators.Length(min=2)])

class MessageForm(FlaskForm):
    text = StringField('Message', [validators.Length(min=2, max=100)])
    user_id = IntegerField('User id')

