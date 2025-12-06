set -e errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

if [[$CREATE_SUPERUSER == "true"]]; then
    python manage.py createsuperuser --noinput
fi
