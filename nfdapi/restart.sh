./manage.py makemigrations
./manage.py migrate
./manage.py compilemessages
./manage.py collectstatic --noinput

sudo systemctl restart slapd
sudo systemctl restart apache2
sudo systemctl restart metroparksnfd.service
sudo systemctl restart uwsgi
