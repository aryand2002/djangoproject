from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile_no, password=None, address=None, user_type='user'):
        if not email:
            raise ValueError('User must have an email address')
        if not mobile_no:
            raise ValueError('User must have a mobile number')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile_no=mobile_no,
            address=address,
            user_type=user_type.lower()
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile_no, password=None):
        user = self.create_user(
            email=email,
            name=name,
            mobile_no=mobile_no,
            password=password,
            address='',
            user_type='admin'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
