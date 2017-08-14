# nfdapi
 
 Cleveland Metroparks - Natural Features Database REST API
 
## Development

Install native requirements (required for Python LDAP modules):
```shell
#Debian/Ubuntu:
sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
RedHat/CentOS:
sudo yum install python-devel openldap-devel
```

Install Python requirements using a virtual environment:
```shell
# create a Python virtual env to install dependences
mkdir venvs ; cd venvs
virtualenv metroparksnfd
# activate the virtual env
source metroparksnfd/bin/activate
# install requirements
pip install -r ../clevmetro-nfd/nfdapi/requirements.txt
```

Setup a PostgreSQL database and enable the PostGIS extension. Adjust the [settings.py](nfdapi/settings.py) file
accordingly:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'metroparksnfd',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Create database schema:

```shell
cd clevmetro-nfd/nfdapi
$ ./manage.py migrate
$ ./manage.py createinitialrevisions
```

Initialize the dictionary tables (using `./manage.py shell`):
```python
from nfdcore import initmodel as i
i.init_model()
```
Optional: Insert some test species:
```python
from nfdcore import initmodel as i
i.insert_test_species()
```

Optional: Insert some test occurrences (Warning: it will delete existing occurrences):
```python
from nfdcore import initmodel as i
i.insert_test_data()
```

Finally, use Eclipse PyDev to edit and run REST API. By default, the application is available
on http://localhost:8000/nfdapi/

We use Django Rest Framework, which offers a nice web interface to test and become familiar with the rest API.
Have a look for instance to the following URLs:

* http://localhost:8000/nfdapi/layers/animal/
* http://localhost:8000/nfdapi/layers/animal/xxx (where xxx is the id of an animal occurrence)

The nfdapi static files have to be generated (using `django-admin collectstatic`)
and copied to
/var/www/clevmetronfd-static to properly see the styles of REST web interface

In addition, you may need to adjust [settings.py](nfdapi/settings.py) to
match your HTTP server file layout:
```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# we need to run django-admin collectstatic whenever dependences are modified or updated
STATIC_ROOT = '/var/www/clevmetronfd-static'
STATIC_URL = '/nfdapi-static/'
```

## Translations

Whenever new translations strings are added to the application, the translation
keys on the .po files must be updated using `django-admin makemessages`.

When the translations are completed, the .po files have to be compiled using
`django-admin compilemessages`.

## Migrations and versioned models

Whenever the data model is modified, Django migrations have to be generated using
`./manage.py makemigrations nfdcore`. The generated migration files have to be commited to the
repository, as they will need to be applied on servers (and the dev environments
of the rest of developers) using `./manage.py migrate`.

In addition, if the new models use versioning, they must be initialized using
`./manage.py createinitialrevisions nfdcore.YourNewModel` command.
