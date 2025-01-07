#!/bin/sh

until python -c "import MySQLdb; MySQLdb.connect(host='${DATABASE_HOST}', port=int('${DATABASE_PORT}'), user='${MYSQL_USER}', passwd='${MYSQL_PASSWORD}', db='${MYSQL_DATABASE}')"; do
    echo "Waiting for MySQL to be ready..."
    sleep 1
done

echo "Database is ready!"

echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2

echo "Applying database migrations..."
python manage.py migrate --noinput

exec gunicorn core.wsgi:application \
  --workers=2 \
  --threads=2 \
  --worker-class=sync \
  --max-requests=1000 \
  --timeout=30 \
  --keep-alive=5 \
  --bind 0.0.0.0:8000 \
  --log-level=info
