### Django demo application install
- `git clone https://github.com/boriskrutskih/news-portal.git`
- `cd news-portal`

   Настройка .env окружения, пример  `.env.example`
-  install pipenv `pip install pipenv`
- `pipenv install`
- `python manage.py makemigrations && python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`


### Запуск Redis для celery
- `docker run -d -p 6379:6379 redis`


### Запуск Celery
- `celery -A newsblog worker --pool=solo -l info`
