from flask import Flask, render_template, request
from forms import ContactForm

app = Flask(__name__)
app.secret_key = 'SEEKRITKEE'

@app.route('/', methods=['GET', 'POST'])
def handle_contact_form():
    """Handle the contact form."""

    form = ContactForm(request.form)

    if request.method == 'POST' and form.validate():
        return 'Form posted.'

    elif request.method == 'GET':
        return render_template('index.html', form=form)

