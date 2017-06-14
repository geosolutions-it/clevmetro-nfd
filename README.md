# clevmetro-nfd
Cleveland Metroparks - Natural Features Database


# Quickstart

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

Create database schema:

```shell
cd clevmetro-nfd/nfdapi
$ ./manage.py makemigrations core
$ ./manage.py migrate
$ ./manage.py createinitialrevisions
```

Initialize some dictionary tables (Using `./manage.py shell`):
```python
from core import initmodel as i
i.init_model()
```

