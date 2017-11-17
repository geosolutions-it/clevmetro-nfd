# nfdapi
 
 Cleveland Metroparks - Natural Features Database REST API

## API operations

The API operations are documented on the
 [project WIKI](https://github.com/geosolutions-it/clevmetro-nfd/wiki/API-operations).
 
## Development

Install native requirements (required for Python LDAP modules):
```shell
#Debian/Ubuntu:
sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
sudo apt-get install -y --no-install-recommends gettext libcairo2 libffi-dev libpango1.0-0 \
  libgdk-pixbuf2.0-0 libxml2-dev libxslt1-dev shared-mime-info
#RedHat/CentOS:
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
./manage.py migrate
./manage.py createinitialrevisions
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

## LDAP configuration

Authentication and authorization is based on LDAP. The file `settings.py` contains the required
configuration for OpenLDAP (enabled by default) and ActiveDirectory (commented by default).
Some additional variable such as AUTH_LDAP_SERVER_URI and AUTH_LDAP_BIND_PASSWORD should also
be adjusted. Check
[django-auth-ldap documentation](http://django-auth-ldap.readthedocs.io) for additional info.

NFD users are expected to be under `ou=users,dc=Metroparks,dc=local` while the groups they
belong are expected under `ou=groups,dc=Metroparks,dc=local` (this can be adjusted on
settings.py).

The following groups are expected:
  nfdadmins, plant_writer, plant_publisher,
  animal_writer,animal_publisher,slimemold_writer, slimemold_publisher,
  fungus_writer,fungus_publisher, naturalarea_writer, naturalarea_publisher

### OpenLDAP installation

Install OpenLDAP server and utils:

```shell
apt-get install slapd ldap-utils
```

Use all the default configuration options on dpkg configuration, except:
```
Omit OpenLDAP server configuration? No
Domain: Metroparks.local 
Organization: Metroparks
Password: [enter a password for your admin user]
```

You can force package configuration using `dpkg-reconfigure -plow slapd` if configuration is not prompted by default.

Then you can load the required groups and some test users using the following commands:
```shell
service slapd stop
slapadd -n 1 -l /opt/clevmetro-nfd/nfdapi/deploy/data.ldif
service slapd start
```

### PHPLdapAdmin installation

PHPLdapAdmin is a convenient web GUI to configure LDAP users and groups. Installation:

```shell
apt-get install slapd phpldapadmin
```

Then edit the following lines in `/etc/phpldapadmin/config.php`:

```
$servers->setValue('server','name','NFD Test LDAP Server');
...
$servers->setValue('server','host','127.0.0.1');
...
$servers->setValue('server','base',array('dc=Metroparks,dc=local'));
...
$servers->setValue('login','bind_id','cn=admin,dc=Metroparks,dc=local');
...
$config->custom->appearance['hide_template_warning'] = true;
```
