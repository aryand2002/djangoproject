import os
import django
from decouple import config

# ✅ Setup Django settings before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploydjango.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = config("DJANGO_SUPERUSER_EMAIL")
name = config("DJANGO_SUPERUSER_NAME")  # optional, if your model requires it
password = config("DJANGO_SUPERUSER_PASSWORD")

# ✅ Check by email instead of username
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, name=name, password=password)
    print("✅ Superuser created successfully.")
else:
    print("ℹ️ Superuser already exists.")
