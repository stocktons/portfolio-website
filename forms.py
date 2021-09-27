from wtforms import StringField, TextAreaField, validators
from flask_wtf import FlaskForm



class ContactForm(FlaskForm):
    """Form to accept name, email, and message."""

    name = StringField("Name", [validators.Required(), validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Required(), validators.Length(min=6, max=35)])
    message = TextAreaField("Message", [validators.Required(), validators.Length(max=250)])
