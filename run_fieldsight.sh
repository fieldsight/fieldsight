#python manage.py migrate --noinput
#python manage.py fieldsight_default_commands
#python manage.py create_default_superuser
python manage.py migrate --noinput
python manage.py delete_permission
#python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8001

