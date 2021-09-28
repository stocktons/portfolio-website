from wtforms import StringField, TextAreaField, validators
from flask_wtf import FlaskForm



class ContactForm(FlaskForm):
    """Form to accept name, email, and message."""

    name = StringField("Name", [validators.Required("Please enter your name.")])
    email = StringField("Email", [validators.Required("Please enter your email."), validators.Length(min=6, max=35, message="Please enter a valid email address.")])
    message = TextAreaField("Message", [validators.Required("Please enter a message."), validators.Length(max=250)])
