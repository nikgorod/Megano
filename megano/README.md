#Запуск сервера

1. redis-server
2. celery -A megano worker -l INFO -P solo
3. python manage.py server