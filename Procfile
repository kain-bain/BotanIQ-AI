release: python manage.py migrate && python manage.py collectstatic --noinput && python seed_plants.py
web: gunicorn botaniq.wsgi:application --bind 0.0.0.0:$PORT --log-file -
