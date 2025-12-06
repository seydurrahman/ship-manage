set -e errexit

pip install -r requirements.txt

<<<<<<< HEAD
python manage.py collectstatic --no-input
=======
python manage.py collectstatic --noinput
>>>>>>> d2f6c12cf59e5672338aeec2b5dbb02790d57f80
python manage.py migrate

if [[$CREATE_SUPERUSER == "true"]]; then
    python manage.py createsuperuser --noinput
fi
