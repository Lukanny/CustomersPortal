#!/bin/sh

until python -c "import MySQLdb; MySQLdb.connect(host='${DATABASE_HOST}', port=int('${DATABASE_PORT}'), user='${MYSQL_USER}', passwd='${MYSQL_PASSWORD}', db='${MYSQL_DATABASE}')"; do
    sleep 1
done

echo "Banco de dados disponível!"

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec gunicorn --workers 4 --bind 0.0.0.0:8000 core.wsgi:application
