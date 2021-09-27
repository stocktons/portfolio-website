from flask import Flask, render_template, request
from forms import ContactForm
from flask_mail import Mail, Message

mail = Mail()

app = Flask(__name__)
app.secret_key = 'SEEKRITKEE'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = ''
app.config["MAIL_PASSWORD"] = ''

mail.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def handle_contact_form():
    """Handle the contact form."""

    form = ContactForm(request.form)
    if request.method == 'GET':
        return render_template('index.html', form=form)

    if request.method == 'POST' and form.validate():
        msg = Message("Contact Form", 
                      recipients="sarah@thanksforallthe.fish", 
                      sender=(form.name.data, form.email.data))
        msg.body = form.message.data
        print(msg, "This is the message object")
        mail.send(msg)
        return render_template('index.html', success=True)
 

    

