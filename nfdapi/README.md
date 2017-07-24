 #nfdapi
 
 Cleveland Metroparks - Natural Features Database REST API
 
 # Development

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

Setup a PostgreSQL database and enable the PostGIS extension. Adjust the settings.py file
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

Optional: Initialize some dictionary tables (Using `./manage.py shell`. Warning: it will delete existing dict tables):
```python
from core import initmodel as i
i.init_model()
```
Optional: Insert some test data (Warning: it will delete existing occurrences):
```python
from core import initmodel as i
i.insert_test_data()
```

Finally, use Eclipse PyDev to edit and run REST API. By default, the application is available
on http://localhost:8000/nfdapi/

We use Django Rest Framework, which offers a nice web interface to test and become familiar with the rest API.
Have a look for instance to the following URLs:
http://localhost:8000/nfdapi/layers/animal/
http://localhost:8000/nfdapi/layers/animal/xxx (where xxx is the id of an animal occurrence)

You may need to adjust [settings.py](nfdapi/settings.py) to properly see the styles of REST web interface:
```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# we need to run django-admin collectstatic whenever dependences are modified or updated
STATIC_ROOT = '/var/www/clevmetronfd-static'
STATIC_URL = '/nfdapi-static/'
```

 # Deployment
The nfdapi application should be deployed on a WSGI compatible web server such as Apache or Nginx.
A [systemd script is provided](deploy/metroparksnfd.service) for deploying nfdapi as a system service
using the uWSGI application
container. uWSGI can be integrated
with Apache or Nginx [using different approaches](http://uwsgi-docs.readthedocs.io/en/latest/WebServers.html).
For the dev server, a simple proxy configuration was used to integrate Apache with uWSGI:

```
# /etc/apache2/conf-enabled/nfdapi.conf 
Header set Access-Control-Allow-Origin "*"
Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
Alias /static /opt/clevmetro-nfd/nfdclient
<Directory "/opt/clevmetro-nfd/nfdclient">
      Order allow,deny
      Allow from all
      Require all granted
</Directory>

Alias /nfdapi-static /var/www/clevmetronfd-static
<Directory "/var/www/clevmetronfd-static">
      Order allow,deny
      Allow from all
      Require all granted
</Directory>

ProxyPass /nfdapi http://localhost:3001/nfdapi
ProxyPassReverse /nfdapi http://localhost:3001/nfdapi
```

