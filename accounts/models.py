from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):    

    GENDER_CHOICES = (
        ("M", "MALE"),
        ("F", "FEMALE"),
        ("O", "PREFER NOT TO SAY"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(upload_to ='profile_pic', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()