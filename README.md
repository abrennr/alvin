# alvin

## 1. Overview

*alvin* is a django app used in-house for doing basic digital media object cataloging.

It's intended to be a temporary solution, transitioning between an older process and something else to come.

## 2. Deployment

### 2.1 Requirements

alvin requires Django [https://www.djangoproject.com/] and the Django application `django_filters` [https://github.com/alex/django-filter]. Django has its own requirements, primarily that Python and a database are installed.  Django can be deployed in a number of ways; we've used WSGI.  For more information on deploying Django itself, see https://docs.djangoproject.com/en/1.5/howto/deployment/ [Django v. 1.5 documentation].

### 2.2 How alvin is distributed

alvin is distributed with three subdirectories:

`alvin` - contains the django application code
`media` - contains the static media files (e.g., css, javascript)
`templates` - contains the django template files

### 2.3 Installation and configuration

The `alvin` and `templates` directories can be installed anywhere you would like on your system, but for security reasons should *not* be in under the web server's document root.  `media` on the other hand, should be in a web-accessible location, either on the same server as django or a separate server dedicated to serving static media. 

If a database for alvin does not already exist, create one now.  You will need the database engine (one of 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'), the database name, the database username, and the database password.  No tables need to be created inside the database; the django `syncdb` command will take care of table creation later.

Once installed, the 'settings.py.example' file in the 'alvin' directory should be copied to 'settings.py' and populated with local values. Update the following fields:
* `DATABASE_ENGINE` value should be database you are using
* `DATABASE_NAME` value should be the name of the database created for this app
* `DATABASE_USER` value should be username for the database
* `DATABASE_PASSWORD` value should be the password for the database user
* `TIME_ZONE` change as appropriate for your location
* `MEDIA_ROOT`
* `MEDIA_URL`
* `ADMIN_MEDIA_PREFIX`
* `ROOT_URLCONF` value should be 'alvin.urls'
* `TEMPLATE_DIRS` value should be the path to when you installed alvin's `template` directory 
* `INSTALLED_APPS` should include `'django_filters'` and `'alvin.core'`

After the settings.py file has been updated, from within the `alvin` directory, run the command:
    python manage.py syncdb
The command should create the necessary tables.  Also, because a file of inital data has been included (`initial_data.json`), the ssyncdb command should load the initial data.  It will do this each time the command is run, overwriting changes that have been made.  To avoid this behavior, remove or rename the `initial_data.json` file.

At this point, the application should be functional.
