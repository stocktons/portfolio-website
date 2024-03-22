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

#### Instance Location
On the Amazon Lightsail homepage, make sure your Instance location matches your geographic region.

#### Pick your instance image
Select a platform: Linux/Unix
Select a blueprint: OS Only - Amazon Linux 2023

Leave the launch script and SSH key pair options as-is
No need to enable Automatic Snapshots now

### Choose your instance plan
dual stack
pick the cheapest price per month

### Identify your instance
Okay to just leave the default name
Ignore tagging options


### Set up your new instance
Go to the home screen and click the box that contains your new instance
#### Networking
- Go to the Networking link in the center
- In the Public IPV4 box, click "Attach static IP" -- this is will ensure that your website always has the same IP address whenever your instance stops and restarts
- Keep the suggested name or pick a new one, click "Create and attach"
- note this: you'll use it to SSH in later, and in your Django app settings

##### IPv4 Firewall
- click "Add rule"
- Edit the rule for HTTP / TCP / 80
	- Click the edit icon
	- Click "Restrict to IP address" while you're building. This prevents others on the internet from discovering your site and filling up your logs with HTTP requests.
	- Go to https://whatismyipaddress.com/ to find what your computer's IPv4 address is. Copy and paste that into the new rule.
	- Click the green check mark next to "Create"
- Add a rule for Custom / TCP / 8000
	- Follow the above steps to restrict to your IP address
- Add a rule for SSH / TCP / 22
	- Same steps as above
	- Okay to leave the Lightsail browser SSH if you want to use their terminal instead of your own

Turn off IPv6

### SSH
Go back to the "Connect" tab, and scroll down to see the link to "Download default key". The default key is unique to your instance in your region. The wording makes it sound like it might be the same key for everyone in the region, but it is truly unique and secure.
- Click the link
- If you're on a Mac, it's going to ask if you want to add it to a keychain. Cancel.
- Move the file to a location where you can find it.
#### Update the permissions on the key file
Right now, it's likely that the file has read permissions granted to everyone. Amazon Linux will detect that and make you secure the file on your computer before proceeding.

Type the following command to view the permissions:
```
ls -l path/to/dir/that/has/key
```

That will output something like:

```
-rw-r--r--@ 1 sarah  staff  1675 Jan 23 20:30 LightsailDefaultKey-us-east-1.pem
```

We want to make this readable only by our user, so type:

```
chmod 400 path/to/dir/that/has/key/LightsailDefaultKey-us-east-1.pem
```

Now, `ls -l path/to/dir/that/has/key` should output something similar to the following. It may end with an @, or not. The important part is that you should see one lonely r at the beginning and nothing else but dashes:

```
-r--------@ 1 sarah  staff  1675 Jan 23 20:30 LightsailDefaultKey-us-east-1.pem
```

Note that the permission string is `-r--------` , indicating that there are no permissions except read for the current user only.

#### Connect to your Lightsail instance from your shell
The final command will look something like:

```
ssh -i /Users/sarah/Projects/keys/LightsailDefaultKey-us-east-1.pem ec2-user@44.221.96.117
```

Let's break it down.

`ssh`: (SSH client) is a program for logging into a remote machine and for executing commands on a remote machine. Read more about ssh by typing `man ssh` into your shell.

`-i`: indicates an identity file, in this case the default key we just downloaded

`/Users/sarah/Projects/keys/LightsailDefaultKey-us-east-1.pem`: The path to my key file. Put your particular path here.

`ec2-user@52.201.197.68`: `ec2-user` is the name of the user created by AWS on your new Amazon Linux instance. Instead of logging in as `root`, you'll log in as `ec2-user`. This user has `sudo` privileges already granted. `52.201.197.68` is the static IP address you created at the beginning of your tutorial.

The first time you connect, you'll get a warning message:
```
The authenticity of host '52.201.197.68 (52.201.197.68)' can't be established.
ED25519 key fingerprint is SHA256:QOBe4EJcPT6NqHd66cYGhjIyMlXsId0BRgH4ARc8UI4.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type "yes" to continue and connect

The output should be:

```
Warning: Permanently added '52.201.197.68' (ED25519) to the list of known hosts.
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
[ec2-user@ip-172-26-6-217 ~]$
```

You're now connected to your Linux server!

If you want to disconnect and return to your own computer's shell, type `exit`.

### Server set-up
Amazon Linux 2023 is based on Fedora Linux.
https://aws.amazon.com/blogs/aws/amazon-linux-2023-a-cloud-optimized-linux-distribution-with-long-term-support/

The package manager for this Linux distribution is `dnf`. You can see all the packages that are pre-installed with `sudo dnf list installed`

Run `sudo dnf upgrade` to make sure you've got the latest versions of everything.

If you prefer to use nano as your editor, that's already installed. I'm going to use vim (also already installed) throughout, but it doesn't matter, just use what's comfortable for you.

I am used to zsh as my default shell. Skip this next section if you're fine with using the default bash.

### make zsh the default shell
`sudo dnf install -y zsh`
`which zsh` -- will give you the path to zsh
`sudo lchsh -i ec2-user` -- will prompt you to enter the path to zsh
restart the shell (`exit`) to see the changes take effect
When the shell restarts, you might be prompted with:

```
This is the Z Shell configuration function for new users, zsh-newuser-install.

You are seeing this message because you have no zsh startup files (the files .zshenv, .zprofile, .zshrc, .zlogin in the directory ~).  This function can help you with a few settings that should make your use of the shell easier.

You can:

(q)  Quit and do nothing.  The function will be run again next time.

(0)  Exit, creating the file ~/.zshrc containing just a comment.
     That will prevent this function being run again.

(1)  Continue to the main menu.

--- Type one of the keys in parentheses ---
```

Type `0` to select that option.

You can verify that you have a `.zshrc` file by typing `cat ~/.zshrc`

That will output something like:

```
# Created by newuser for 5.8.1
```

and you can confirm that you are using `zsh` by typing `echo $SHELL`

That should output:

```
/usr/bin/zsh
```

### install  packages
```
sudo dnf install python3-pip python3-devel postgresql15 libpq-devel postgresql15-server nginx gcc
```

These include packages for pip, postgresql, and nginx, and some that help compile C code (necessary for psycopg2).

if the versions change and something doesn't work, use `dnf search python | grep devel` or similar to find the newer version. Note that you will find something like `python3-devel.x86_64` - you CAN type the whole thing like
```
sudo dnf install python3-devel.x86_64
```
but it's also just fine to leave off the `.x86_64` part, as in the commands above.

Type `y` to install the packages.
### PostgreSQL
Begin by initializing the PostgreSQL database:
```
sudo postgresql-setup initdb
```

Start the service:
```
sudo systemctl start postgresql
```

Confirm that it's running without errors:
```
sudo systemctl status postgresql
```

Press `q` to exit out of the status report.

In the next section, we're going to take advantage of peer authentication in PostgreSQL. What this means is, if our postgreSQL user and our Linux system user have the same name, there is no need to grant privileges or use a password.

Create a postgres user whose name matches the default Amazon username:

```
cd /tmp
sudo -u postgres createuser -s $(whoami)
cd -
```

In the above command, we cd into the `/tmp` directory because that directory behaves a little differently than others and won't cause our terminal to spit out warnings after running the commands.

`$(whoami)` is just a convenient way to make sure your new database username EXACTLY matches your Amazon Linux username, with no typos. We're using the command line to create our postgres user here, instead of doing it in psql because we can use the `$(whoami)` shell variable, and also, the permissions are a bit looser, so we'll be able to create a username that contains a hyphen, like `ec2-user`.

`cd -` just returns us to the directory we were in prior to entering the `tmp` directory.

Start up the interactive PostgreSQL terminal and connect to the postgres database. This isn't a database we'll be using, but you have to connect to something to start.

```
psql postgres
```


Create the database you'll use for your project:
```
CREATE DATABASE myproject;
```


And add some configurations recommended by Django:
```
ALTER ROLE "ec2-user" SET client_encoding TO 'utf8';
ALTER ROLE "ec2-user" SET default_transaction_isolation TO 'read committed';  ALTER ROLE "ec2-user" SET timezone TO 'UTC';
```

Quit out of the psql session:
```
\q
```

When you need to log in to your new database:
```
psql myproject
```


### Create a virtual environment for the Django project
In the shell:
```
mkdir ~/myprojectdir
cd ~/myprojectdir
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install django gunicorn psycopg2
```

### Start the new Django project
```
django-admin startproject myproject .
```
The dot here is important, because it's telling Django to create its folder system in the directory that already exists instead of creating another level. Here, `myproject` will be the inner folder inside the `myproject` folder you just created. It's okay to name it something different, or keep it the same.

### settings.py

We'll need to use some environment variables in the `settings.py`, so let's start by setting up a `.env` file. In the outer project folder that contains the `settings.py` file:
```
vim .env
```
This will create a new file called `.env` and open it up in the vim editor.

Before you go any further, let's make sure this file never gets into version control:

```
echo .env >> .gitignore
```
This adds `.env` to the list of files ignored by Git. If the `.gitignore` file doesn't exist yet, it will be created now.

Make sure it's there:
```
cat .gitignore
```
The output should include `.env`

Add the following to your `.env` file:
```
SECRET_KEY=aRandomStringToBeUsedByDjango
```

Save and quit.

Make sure you are in the inner directory, and open the already-existing settings.py file:
```
vim settings.py
```

At the top of the file, add:
```
import os
```

Update the `SECRET_KEY`:
```
SECRET_KEY = os.environ.get("SECRET_KEY")
```

Update the `ALLOWED_HOSTS` block:
```
	ALLOWED_HOSTS = ['localhost', '<your lightsail static IP address>']
```


Alter the `DATABASES` block:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
    }
}
```

Set the location of the static files for when `collectstatic` is run. This is important to be able to point Nginx at it later. You can add this under `STATIC_URL` in the file.

```
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```

Save and close.



Make sure you are in the outer project directory with the `manage.py` file.
Make the migrations:
```
python3 manage.py makemigrations
```

Apply the migrations:
```
python3 manage.py migrate
```

Create a superuser:
```
python3 manage.py createsuperuser
```

Collect the static files:
```
python3 manage.py collectstatic
```

Test the development server:
```
python3 manage.py runserver 0.0.0.0:8000
```

In your web browser, visit your AWS static IP address at port 8000:
```
http://<aws_static_ip>:8000

# something like:
http://123.45.67:8000
```

You should see the Django rocket and be able to visit `http://<aws_static_ip>:8000/admin` and log in to the admin page with the superuser credentials you entered.

Shut down the development server with ctrl-C.

Make it so postgresql will start automatically whenever your server starts up:

research this !

### Gunicorn
Test that Gunicorn is able to serve the application:
```
cd ~/myproject
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
```

Go to the web browser and visit `http://aws_static_ip:8000` once again and it should still work. Going to the `/admin` endpoint will show some broken styling since Gunicorn isn't going to serve up the static files. Your terminal will also show a bunch of errors:
```
Not Found: /static/admin/img/icon-yes.svg
Not Found: /static/admin/img/sorting-icons.svg
Not Found: /static/admin/css/forms.css
Not Found: /static/admin/js/calendar.js
Not Found: /static/admin/js/admin/DateTimeShortcuts.js
Not Found: /static/admin/js/SelectBox.js
Not Found: /static/admin/js/SelectFilter2.js
Not Found: /static/admin/js/prepopulate_init.js
Not Found: /static/admin/js/change_form.js
Not Found: /static/admin/img/icon-deletelink.svg
```

If you can see your website, all is well.

Shut the server down with ctrl-C, and deactivate your `venv` by typing `deactivate`

### Create systemd Socket and Service  Files for Gunicorn

From the digital ocean tutorial:
```
You have tested that Gunicorn can interact with our Django application, but you should now implement a more robust way of starting and stopping the application server. To accomplish this, you’ll make systemd service and socket files.

The Gunicorn socket will be created at boot and will listen for connections. When a connection occurs, systemd will automatically start the Gunicorn process to handle the connection.

Start by creating and opening a systemd socket file for Gunicorn with `sudo` privileges:
```

```
sudo vim /etc/systemd/system/gunicorn.socket
```

Inside the file, type:

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Save and close.

Create the service file:
```
sudo vim /etc/systemd/system/gunicorn.service
```

Inside it, add:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ec2-user # your Linux username
Group=nginx
WorkingDirectory=/home/ec2-user/madlibs # your outer django project dir
ExecStart=/home/ec2-user/madlibs/venv/bin/gunicorn \ # path to gunicorn
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          madlibs.wsgi:application

[Install]
WantedBy=multi-user.target
```


Start and enable the Gunicorn socket:
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```


```
ec2-user@ip-172-26-6-217 ~ % sudo systemctl enable gunicorn.socket

Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.
```

Confirm success:
```
sudo systemctl status gunicorn.socket
```

Press `q` to exit out of the message

Check that the socket file was created by Gunicorn:
```
file /run/gunicorn.sock
```

If you don't find the file, or get other errors, check the logs with:
```
sudo journalctl -u gunicorn.socket
```

We've confirmed that the socket exists and works, but now we need to test that the service starts up when a connection request is received. Confirm that the service isn't started:
```
sudo systemctl status gunicorn
```
Press `q` to exit the message.

Test the socket activation mechanism:
```
curl --unix-socket /run/gunicorn.sock localhost
```

You should see the html of your Django starter page.

```
sudo systemctl status gunicorn
```
Should now show as active.

If there are problems, check the logs:

```
sudo journalctl -u gunicorn
```

If you need to edit the service file, reload the daemon and restart gunicorn:
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Make sure everything is working without errors before proceeding!


### Nginx
We're going to configure Nginx a bit more modularly than is necessary for this small project, but it's a good pattern to know about for future, more complicated setups. It's also the way that Ubuntu-based Nginx comes configured out of the box, so it's useful to understand this way.

Start by creating two directories:
```
sudo mkdir /etc/nginx/{sites-available,sites-enabled}
```

Check that they are there:
```
ls /etc/nginx
```

Create file called proxy_params:
```
sudo vim /etc/nginx/proxy_params
```

In that file, paste:
```
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```
Save and quit

Create a new file in the sites-available directory:
```
sudo vim /etc/nginx/sites-available/myprojectname
```

Inside that file, paste:
```
server {
    listen 80;
    server_name <aws_static_ip_address>;
    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ec2-user/madlibs;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

```

Open up the Nginx configuration file:
```
sudo vim /etc/nginx/nginx.conf
```

In that file, find the line
```
include /etc/nginx/conf.d/*.conf;
```
And right after it, add:
```
include /etc/nginx/sites-enabled/*;
```

Lastly, create a symlink to your site config file that you created in `sites-available` and put it in `sites-enabled`

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

```
ls /etc/nginx/sites-available
```
will show your actual file, and
```
ls /etc/nginx/sites-enabled
```
will show the symlink, ready to be read by the `nginx.conf` file.

Test your Nginx configuration for errors:
```
sudo nginx -t
```

If it reports success, go ahead and restart Nginx:
```
sudo systemctl restart nginx
```

### Adjust permissions
Add Nginx's user to your Linux system user's group:
```
sudo usermod -aG linuxusername nginx
```
This will allow Nginx to execute anything owned by `ec2-user`

And make it so only our user has full permissions, and the group can only execute, and anyone else can't do anything:
```
chmod 710 /home/ec2-user
```

### HTTPS with Let's Encrypt

Start by installing Certbot and its Nginx plugin:
```
sudo dnf install certbot python3-certbot-nginx
```

Go into your Amazon Lightsail dashboard, and under the Networking tab, add a rule to the IPv4 Firewall for HTTPS. You can restrict it to your own IP address for now, if you wish.

#### Set up DNS records with your domain name seller
Go to your domain name seller, and add an A record that points to your AWS static IP address. Add one for both `yourwebsite.com` and `www.yourwebsite.com`

Give it a few minutes, and check on the DNS propagation status with `dig`:
```
dig madlibs.sarahstockton.dev
```

Look for the "Answer Section":
```
;; ANSWER SECTION:

yourwebsite.com. 60 IN A 12.345.67.890
```
This tells you that `yourwebsite.com` has successfully been associated with your AWS static IP - 60 is the number of seconds for TTL, your number may be different, and that's fine

#### Change your nginx file to use your hostname instead of the IP:
```
sudo vim /etc/nginx/sites-available/yourproject
```

replace the `server_name` line with all the hostnames you added to your domain name seller records:
```
server_name yourwebsite.com www.yourwebsite.com
```
Save and quit.

#### Add your hostname(s) to ALLOWED_HOSTS
```
vim /home/ec2-user/myproject/myproject/settings.py
```
Add your hostnames to ALLOWED_HOSTS

#### Toggle DEBUG
While you're in `settings.py`, set `DEBUG=False`
#### Make port 80 accessible
If you chose to make requests to port 80 accessible only by your IP address in your Lightsail instance's IPv4 Firewall rules, go to your account and lift that restriction now. Even though port 80 is for HTTP, Certbot will use port 80 and make the necessary adjustments for HTTPS.

#### Request an SSL certificate
```
sudo certbot --nginx -d your_domain -d www.your_domain
```
You can use the `-d` flag to add as many domains and subdomains as needed.

The success message:
```
Saving debug log to /var/log/letsencrypt/letsencrypt.log

Requesting a certificate for madlibs.sarahstockton.dev and www.madlibs.sarahstockton.dev



Successfully received certificate.

Certificate is saved at: /etc/letsencrypt/live/madlibs.sarahstockton.dev/fullchain.pem

Key is saved at:         /etc/letsencrypt/live/madlibs.sarahstockton.dev/privkey.pem

This certificate expires on 2024-04-27.

These files will be updated when the certificate renews.

Certbot has set up a scheduled task to automatically renew this certificate in the background.



Deploying certificate

Successfully deployed certificate for madlibs.sarahstockton.dev to /etc/nginx/sites-enabled/madlibs

Successfully deployed certificate for www.madlibs.sarahstockton.dev to /etc/nginx/sites-enabled/madlibs

Congratulations! You have successfully enabled HTTPS on https://madlibs.sarahstockton.dev and https://www.madlibs.sarahstockton.dev
```

Restart your server to refresh everything.

You can visit https://yoursite.com/admin and see the admin panel!

If you have an empty Django project, you'll see a 404 page on https://yoursite.com/ because you're not serving anything there.

### Add security settings to settings.py
See Django's recommended security settings by running:
```
python3 manage.py check --deploy
```

### Logging
Non-Django logs:
The following logs may be helpful:

- Check the Nginx process logs by typing: `sudo journalctl -u nginx`
- Check the Nginx access logs by typing: `sudo less /var/log/nginx/access.log`
- Check the Nginx error logs by typing: `sudo less /var/log/nginx/error.log`
- Check the Gunicorn application logs by typing: `sudo journalctl -u gunicorn`
- Check the Gunicorn socket logs by typing: `sudo journalctl -u gunicorn.socket`

Django logs:
When in production, you can't just `print(variable)` and see it in the terminal. Instead, we can set up some logging to accomplish this, and to capture other events as well.

- create the log file where you'd like it to live
- change group ownership to a group that ec2-user is part of, `adm`
- change permissions so that owner and group can read and write, no global permissions
```
sudo touch /var/log/django.log
sudo chown root:adm /var/log/django.log
sudo chmod 660 /var/log/django.log
```

In `settings.py`, create a `Logging` block:
```
# at the top
import logging

.
.
.
.

# LOGGING
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/var/log/django.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}
```

Now, when you want to examine something that's happening in your code, you can:
```
import logging

logger = logging.getLogger(__name__)

logger.debug(f"some_string: {my_variable_or_expression}")

```

You cannot log in `settings.py`! Don't try.

More about logging: https://docs.djangoproject.com/en/5.0/howto/logging/#naming-loggers






Clear a log file (or any file):
```
truncate -s 0 django.log
```
`-s 0` == size of 0


### Git and GitHub
```
sudo dnf install git
```

Inside the project folder:
```
echo venv/ >> .gitignore
echo __pycache__ >> .gitignore
cat .gitignore
```
MAKE SURE YOUR `.env` file is listed there!!!! (`venv/` and `__pycache__` should be as well)


```
git init
```

You might be asked:
```
zsh: correct 'git' to '_git' [nyae]?
```
Type `n`

You'll get confirmation:
```
hint: Using 'master' as the name for the initial branch. This default branch name

hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: git branch -m <name>
```

And your command line should look like:
```
ec2-user@ip-172-26-6-217 master ~/madlibs %
```


Let's rename master to main by following the last hint:
```
git branch -m main
```

and now your command line will look like:
```
ec2-user@ip-172-26-6-217 main ~/madlibs %
```


Back in your terminal make an initial commit:
```
git add .
# take a scan through a make triple sure your .env is not listed!!
git commit -m "initial commit"
```

We're going to connect to GitHub via SSH rather than HTTP. To do so, we'll need to generate an SSH key. Read more here: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

In your terminal:
```shell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

You'll get a message:
```shell
Generating public/private ed25519 key pair.

Enter file in which to save the key (/home/ec2-user/.ssh/id_ed25519):
```
hit Enter to accept the default path
if you don't want a passphrase, hit Enter twice
```shell
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/ec2-user/.ssh/id_ed25519
Your public key has been saved in /home/ec2-user/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:07Hnc2c65+fL4Reg7glo+kYr1IHvOO5XZDbHbavBPsk sarah@thanksforallthe.fish
The key's randomart image is:
+--[ED25519 256]--+
|                 |
|                 |
|      .   o .    |
|     . . * = +   |
|      o S * + o  |
|     . +.o * . . |
|    . +oo.+ * ..+|
|     +o=  .E.o++=|
|    o+*.  .o. .O*|
+----[SHA256]-----+
```

In your terminal:
```
cat /home/ec2-user/.ssh/id_ed25519.pub
```
Copy the result to your clipboard, and go to:
https://github.com/settings/keys
And click "New SSH key"
Add a Title to identify your server
Select "Authentication Key" under Key Type
and paste your key into the box
Click "Add SSH key"

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

Back in your terminal, we're going to configure git to use your name and email rather than the default ec2-user info:
```
git config --global --edit
```
use your github username for name, and your email address for email.

In GitHub, create a new repo and give it a name.
Make sure the SSH box is selected under "Quick Setup"
copy the address in "Quick Setup"
In your terminal

```
git remote add origin <copied address>
git push -u origin main
```

You'll get a message like:
```
Enumerating objects: 153, done.
Counting objects: 100% (153/153), done.
Delta compression using up to 2 threads
Compressing objects: 100% (116/116), done.
Writing objects: 100% (153/153), 362.86 KiB | 90.71 MiB/s, done.
Total 153 (delta 33), reused 153 (delta 33), pack-reused 0
remote: Resolving deltas: 100% (33/33), done.
To github.com:stocktons/madlibs.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

### Security
Add some middleware for CSP protection:
https://django-csp.readthedocs.io/en/latest/installation.html

Add it to the `MIDDLEWARE` section of `settings.py` . Configure it with: `CSP_DEFAULT_SRC = ("'self'",)` or whatever you deem best after reading up on all the settings.

Test that your site is secure against:
`observatory.mozilla.org`

Install `security` : https://github.com/pyupio/safety
And run a scan. Best done from a local computer, not a remote server, since it will try to pop open a browser for authentication.

### VSCode SSH
---NOT WORTH IT---
download the extension:
https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh

In VSCode:
cmd + shift + P
Open SSH configuration file: `/Users/sarah/.ssh/config`
```
Host Madlibs_Server
	HostName 44.221.96.117
	User ec2-user
	IdentityFile /Users/sarah/Projects/keys/LightsailDefaultKey-us-east-1-amazon-linux-2.pem
```
cmd + shift + P -- connect to host

to close:
File: Close Remote Connection or cmd + shift + p, same
## Troubleshooting
See stacktrace for server 500 errors with `pym check`

=================


upon trying to log in as an admin user ONLY IN INSOMNIA!

```

# Forbidden (403)

CSRF verification failed. Request aborted.

You are seeing this message because this HTTPS site requires a “Referer header” to be sent by your web browser, but none was sent. This header is required for security reasons, to ensure that your browser is not being hijacked by third parties.

If you have configured your browser to disable “Referer” headers, please re-enable them, at least for this site, or for HTTPS connections, or for “same-origin” requests.

If you are using the <meta name="referrer" content="no-referrer"> tag or including the “Referrer-Policy: no-referrer” header, please remove them. The CSRF protection requires the “Referer” header to do strict referer checking. If you’re concerned about privacy, use alternatives like <a rel="noreferrer" …> for links to third-party sites.

## Help

Reason given for failure:

    Referer checking failed - no Referer.


In general, this can occur when there is a genuine Cross Site Request Forgery, or when [Django’s CSRF mechanism](https://docs.djangoproject.com/en/4.2/ref/csrf/) has not been used correctly. For POST forms, you need to ensure:

- Your browser is accepting cookies.
- The view function passes a `request` to the template’s [`render`](https://docs.djangoproject.com/en/dev/topics/templates/#django.template.backends.base.Template.render) method.
- In the template, there is a `{% csrf_token %}` template tag inside each POST form that targets an internal URL.
- If you are not using `CsrfViewMiddleware`, then you must use `csrf_protect` on any views that use the `csrf_token` template tag, as well as those that accept the POST data.
- The form has a valid CSRF token. After logging in in another browser tab or hitting the back button after a login, you may need to reload the page with the form, because the token is rotated after a login.

You’re seeing the help section of this page because you have `DEBUG = True` in your Django settings file. Change that to `False`, and only the initial error message will be displayed.

You can customize this page using the CSRF_FAILURE_VIEW setting.



```


==================
```
(venv) ec2-user@ip-172-26-6-217 ~/madlibs % pym check --deploy

System check identified some issues:



WARNINGS:

**?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.**

**?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.**

**?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.**

**?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.**

**?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.**

**?: (security.W018) You should not have DEBUG set to True in deployment.**


**2nd try**

WARNINGS:

**?: (security.W005) You have not set the SECURE_HSTS_INCLUDE_SUBDOMAINS setting to True. Without this, your site is potentially vulnerable to attack via an insecure connection to a subdomain. Only set this to True if you are certain that all subdomains of your domain should be served exclusively via SSL.**

**?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.**

**?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.**

**?: (security.W021) You have not set the SECURE_HSTS_PRELOAD setting to True. Without this, your site cannot be submitted to the browser preload list.**
```

==================

Troubleshooting:
```
sudo cat /var/lib/pgsql/data/log/postgresql-Thu.log
```


===================
Great diagrams and explanation of Nginx with Django ( and more links at the bottom of the article ): https://mattsegal.dev/nginx-django-reverse-proxy-config.html


TODO:
sudoers file to need the ec2-user password for sudo
Logging
Block malicious IPs (multiple log in attempts)
Start postgresql automatically





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
