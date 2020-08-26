release: python manage.py migrate --noinput
web: daphne hands.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker -A hands -l info -Q default,low_priority,saving --autoscale 16,4 -n worker@%h
worker_high: celery worker -A hands -l info -Q high_priority,default,liking --autoscale 16,4 -n worker_high@%h
beat: celery beat -A hands -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
longreadbot: apt-get install poppler-utils && python run_bot.py