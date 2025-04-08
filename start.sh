#!/bin/sh

set -e  # Exit on error

# Set default values if not provided
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Wait for the DB to be ready
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ PostgreSQL is available"

# Apply migrations and collect static files
echo "🚀 Running Django setup tasks..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "👤 Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME:-admin}"
email = "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
password = "${DJANGO_SUPERUSER_PASSWORD:-admin123}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created.")
else:
    print("ℹ️ Superuser already exists.")
EOF

# Start Daphne server
echo "🌀 Starting Daphne server..."
daphne -b 0.0.0.0 -p 8000 core.asgi:application
