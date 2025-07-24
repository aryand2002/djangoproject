import os
import django
from decouple import config

# ✅ Setup Django settings before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploydjango.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = config("DJANGO_SUPERUSER_USERNAME")
email = config("DJANGO_SUPERUSER_EMAIL")
password = config("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created successfully.")
else:
    print("ℹ️ Superuser already exists.")
