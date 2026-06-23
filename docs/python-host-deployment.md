# Python Host Deployment

Set production environment variables, install dependencies, run migrations, collect static files, and serve with Gunicorn or the host WSGI runner.

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --config gunicorn.conf.py
```
