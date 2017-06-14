# clevmetro-nfd
Cleveland Metroparks - Natural Features Database


# Quickstart

Create database schema:

```shell
$ ./manage.py makemigrations core
$ ./manage.py migrate
$ ./manage.py createinitialrevisions
```

Initialize some dictionary tables (Using `./manage.py shell`):
```python
from core import initmodel as i
i.init_model()
```

