./manage.py createinitialrevisions

sudo systemctl restart slapd
sudo systemctl restart apache2
sudo systemctl restart metroparksnfd.service
sudo systemctl restart uwsgi
