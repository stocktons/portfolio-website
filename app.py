from flask import Flask, render_template, request, flash
from flask_compress import Compress
from forms.forms import ContactForm
from flask_mail import Mail, Message
from flask_moment import Moment
import os
import markdown
import markdown.extensions.fenced_code
import sqlite3

app = Flask(__name__)
Compress(app)
moment = Moment(app)

app.secret_key = 'SEEKRITKEE'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = 'sarah@thanksforallthe.fish'
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PW")
app.config["RECAPTCHA_USE_SSL"] = False
app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get("RECAPTCHA_PUBKEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get("RECAPTCHA_SECRETKEY")
app.config["RECAPTCHA_OPTIONS"] = {'theme': 'white'}

mail = Mail(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def handle_contact_form():
    """Handle the contact form."""

    form = ContactForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            flash('Oops! Something\'s not quite right with your submission.')
            return render_template('index.html', form=form)
        else:
            """Send Email."""
            msg = Message("Website Contact Form",
                          recipients=["sarah@thanksforallthe.fish"],
                          sender=(form.name.data, form.email.data))
            msg.body = f"Name: {form.name.data} \n Email: {form.email.data} \n Message: {form.message.data}"
            mail.send(msg)

            """Reset form after sending email."""
            form.name.data = ""
            form.email.data = ""
            form.message.data = ""

            return render_template('index.html', form=form, success=True)

    elif request.method == 'GET':
        return render_template('index.html', form=form)


@app.get('/articles')
def list_articles():
    """Displays list of all articles."""

    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()

    return render_template('articles.html', articles=articles)


@app.get('/articles/<slug>')
def show_article(slug):
    """Display requested article from markdown content."""

    conn = get_db_connection()
    article_row = conn.execute(
        'SELECT content, title FROM articles WHERE slug = ?',
        (slug,)
    ).fetchone()
    conn.close()

    md_template_string = markdown.markdown(
        article_row[0],
        extensions=["fenced_code"]
    )

    title = article_row[1]

    return render_template(
        'article.html',
        content=md_template_string,
        title=title
    )
