from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField

class UserModel(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User')
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=200)

    mobile_no = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+91\d{10}$',
                message="Mobile number must be in the format +91XXXXXXXXXX"
            )
        ]
    )

    address = models.CharField(max_length=300, blank=True, null=True)  # ✅ New field

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='user'  # ✅ Default set to 'user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no']

    def __str__(self):
        return f"{self.email} ({self.user_type})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        if self.mobile_no and not self.mobile_no.startswith('+91'):
            self.mobile_no = '+91' + self.mobile_no[-10:]
        super().save(*args, **kwargs)

class Decoration(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name