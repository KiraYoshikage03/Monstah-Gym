from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import UUIDField
from django.utils import timezone
import uuid

# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, user_name, password, **other_fields)
    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email adress')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email


class Monthly(models.Model):
    user_monthly = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name = "monthly_user")
    unique_id = models.CharField(max_length=8, blank=True, unique=True, editable=False)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    email = models.ForeignKey(User, null=True, to_field='email', on_delete=models.CASCADE, related_name="monthly_email")
    weight = models.CharField(max_length=150, blank=True, null=True)
    height = models.CharField(max_length=150, blank=True, null=True)
    em_fullname = models.CharField(max_length=150, blank=True, null=True)
    relationship = models.CharField(max_length=150, blank=True, null=True)
    em_contactno = models.BigIntegerField(blank=True, null=True)
    em_email = models.EmailField(blank=True, null=True)
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    renew = models.ImageField(upload_to='images/', blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    ss_email = models.ImageField(upload_to='images/', blank=True, null=True)
    payment = models.ImageField(upload_to='images/', blank=True, null=True)
    is_cancel = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    renew_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email.email
    # verified_objects = VerifiedUsersManager() 
    # nverified_objects = NotVerifiedUsersManager() 


class Annual(models.Model):
    user_annual = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="annual_user")
    unique_id = models.CharField(max_length=8, blank=True, unique=True, editable=False)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    email = models.ForeignKey(User, null=True, to_field='email', on_delete=models.CASCADE, related_name="annual_email")
    weight = models.CharField(max_length=150, blank=True, null=True)
    height = models.CharField(max_length=150, blank=True, null=True)
    em_fullname = models.CharField(max_length=150, blank=True, null=True)
    relationship = models.CharField(max_length=150, blank=True, null=True)
    em_contactno = models.BigIntegerField(blank=True, null=True)
    em_email = models.EmailField(blank=True, null=True)
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    renew = models.ImageField(upload_to='images/', blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    ss_email = models.ImageField(upload_to='images/', blank=True, null=True)
    payment = models.ImageField(upload_to='images/', blank=True, null=True)
    is_cancel = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    renew_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email.email
    

class Custom(models.Model):
    user_custom = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="custom_user")
    unique_id = models.CharField(max_length=8, blank=True, unique=True, editable=False)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    email = models.ForeignKey(User, null=True, to_field='email', on_delete=models.CASCADE, related_name="custom_email")
    weight = models.CharField(max_length=150, blank=True, null=True)
    height = models.CharField(max_length=150, blank=True, null=True)
    em_fullname = models.CharField(max_length=150, blank=True, null=True)
    relationship = models.CharField(max_length=150, blank=True, null=True)
    em_contactno = models.BigIntegerField(blank=True, null=True)
    em_email = models.EmailField(blank=True, null=True)
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    renew = models.ImageField(upload_to='images/', blank=True, null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    ss_email = models.ImageField(upload_to='images/', blank=True, null=True)
    payment = models.ImageField(upload_to='images/', blank=True, null=True)
    is_cancel = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    renew_startdate = models.DateField(blank=True, null=True)
    renew_enddate = models.DateField(blank=True, null=True)
    renew_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email.email
    
    