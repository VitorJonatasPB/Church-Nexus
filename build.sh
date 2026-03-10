#!/usr/bin/env bash
# build.sh
set -o errexit

pip install -r backend/requirements.txt

cd backend
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "from django.contrib.auth import get_user_model; import os; User = get_user_model(); User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists() or User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_EMAIL'), os.environ.get('DJANGO_SUPERUSER_PASSWORD'))"
