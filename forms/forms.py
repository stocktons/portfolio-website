from wtforms import StringField, TextAreaField, validators
from flask_wtf import FlaskForm
from wtforms.validators import Email 

class ContactForm(FlaskForm):
    """Form to accept name, email, and message."""

    name = StringField("Name", [validators.Required()])
    email = StringField("Email", [Email(message="Not a valid email address."), validators.Required()])
    message = TextAreaField("Message", [validators.Required(), validators.Length(max=1000)])
