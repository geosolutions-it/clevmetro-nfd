# clevmetro-nfd
Cleveland Metroparks - Natural Features Database

## Overview

The software is composed of a [client application](nfdclient/README.md) based on MapStore2, React and Redux technologies,
and a [REST API](nfdapi/README.md) based on Django. Have a look at both subprojects for detailed development and
deployment documentation.

## Deployment 

Clone the repository with the --recursive option to automatically clone submodules:

`git clone --recursive https://github.com/geosolutions-it/clevmetro-nfd.git`

Then configure Apache or Nginx to serve the nfdclient application on the root
("/") path and the nfdapi Django application on "nfdapi/" path.

The client application is served as static content.

The nfdapi application should be served using a WSGI compatible web server such as Apache or Nginx.
A [systemd script is provided](nfdapi/deploy/metroparksnfd.service) for deploying nfdapi as a system service
using the uWSGI application container. uWSGI can be integrated
with Apache or Nginx [using different approaches](http://uwsgi-docs.readthedocs.io/en/latest/WebServers.html).
For the dev server, a simple proxy configuration was used to integrate Apache with uWSGI.

The following configuration file can be used to configure Apache for
nfdclient and nfdapi applications:

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

Have a look to the specific [nfdapi readme file](nfdapi/README.md) for
additional configuration steps (required for develoment and deployment
envs).
