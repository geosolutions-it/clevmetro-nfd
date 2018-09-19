./manage.py makemigrations
./manage.py migrate
./manage.py compilemessages
./manage.py collectstatic --noinput

sudo initctl restart metroparksnfd-uwsgi
