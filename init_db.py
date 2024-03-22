import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO articles (title, slug, content) VALUES (?, ?, ?)",
    (
        'Deploying a Django App on Amazon Lightsail',
        'deploying-a-django-app-on-amazon-lightsail',
        '''
** note that some outputs may differ than what is shown depending on your terminal setup
### Create a new Lightsail instance

.....

## Tutorial Sections
1. Lightsail/SSH
2. Server/shell/Django
3. Gunicorn and Nginx
4. HTTPS & security settings
5. Git and GitHub
6. '''
    )
)

cur.execute("INSERT INTO tags (tag) VALUES (?)",
            ('devops',)
            )

cur.execute("INSERT INTO articles_tags (tag_id, article_id) VALUES (?, ?)",
            (1, 1)
            )

connection.commit()
connection.close()
