web: gunicorn -b "0.0.0.0:$PORT" -w 3 retailshop.wsgi
release: python manage.py migrate
