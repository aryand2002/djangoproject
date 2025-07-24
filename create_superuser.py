import os
import django
from decouple import config

# ✅ Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploydjango.settings')  # update if your project name is different
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Read env variables
email = config("DJANGO_SUPERUSER_EMAIL")
name = config("DJANGO_SUPERUSER_NAME", default="Admin")
mobile_no = config("DJANGO_SUPERUSER_MOBILE", default="+911234567890")
password = config("DJANGO_SUPERUSER_PASSWORD")

# ✅ Check and create superuser
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        name=name,
        mobile_no=mobile_no,
        password=password
    )
    print("✅ Superuser created successfully.")
else:
    print("ℹ️ Superuser already exists.")
