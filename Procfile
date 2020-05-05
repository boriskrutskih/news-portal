web: gunicorn newsblog.wsgi --log-file -
worker: celery -A newsblog worker --pool=solo -l info