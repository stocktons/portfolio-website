
from wtforms import StringField, TextAreaField, validators
from flask_wtf import Form


class ContactForm(Form):
    """Form to accept name, email, and message."""

    name = StringField("Name", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=35)])
    message = TextAreaField("Message", [validators.Length(max=250)])
