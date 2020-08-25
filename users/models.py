from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser#, BaseUserManager
from .managers import UserManager
from django.core.validators import RegexValidator
import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#password reset
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

sex = [
    ('Male','Male'),
    ('Female','Female'),
]
USERNAME_REGEX = '^[a-za-z0-9]+$'
CP_NUMBER_REGEX='^(09|\+639)\d{9}$'
NAME_REGEX = '^[a-zA-Z ]+$'

#from PIL import Image

class User(AbstractBaseUser):
    username = models.CharField(
                    max_length=150,
                    validators = [
                        RegexValidator(regex = USERNAME_REGEX,
                                        message = 'Username must be alphanumeric or contain numbers and lowercaps',
                                        code='invalid_username'
                            )],
                    unique=True
        )
    email		    =models.EmailField(max_length = 255,null=True,blank=True, unique=True)
    first_name 	    =models.CharField(max_length=255, null=True, blank=False,
                    validators = [RegexValidator(regex = NAME_REGEX,
                                    message = 'First name must be letters only',
                                    code = 'invalid_first_name'
                    )]
        )
    # middle_name =models.CharField(max_length=255, null=True, blank=True,
    #                 validators = [RegexValidator(regex = NAME_REGEX,
    #                                 message = 'Middle name must be letters only',
    #                                 code = 'invalid_middle_name'
    #                 )]
    #     )
    last_name 	    =models.CharField(max_length=255, null=True, blank=False,
                    validators = [RegexValidator(regex = NAME_REGEX,
                                    message = 'Last name must be letters only',
                                    code = 'invalid_last_name'
                    )]
        )
    active		    = models.BooleanField(default=True) # can login 
    staff		    = models.BooleanField(default=False) # non-super user
    admin		    = models.BooleanField(default=False) # superuser
    timestamp	    = models.DateTimeField(auto_now=False, auto_now_add=True)

    USERNAME_FIELD = 'username' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects              = UserManager()

    def __str__(self):
        return self.username

    def get_total_user(self):
        return self.User.objects.all().count()

    # def get_age(self):
    #     current_year = datetime.date.today().year
    #     dateofbirth_year = self.birthday.year
    #     if dateofbirth_year:
    #         return current_year - dateofbirth_year
    #     return

    def get_user_type(self):
        if self.is_admin:
            return "Admin"
        if self.is_staff:
            return "Staff"
        if self.is_active:
            return "User"

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.username

    # def get_middle_name(self):#
    #     if self.middle_name:
    #         return self.middle_name
    #     return self.middle_name

    # def get_middle_initial(self):
    #     self.middle_name = self.middle_name.split()[0:1]
    #     return self.middle_name

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.username

    def has_perm(self, perm, obj=None): # required
        return True

    def has_module_perms(self, app_label): # required
        return True

    

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 

class Profile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio                 = models.TextField(blank=True, null=True)
    gender		        =models.CharField(max_length=100,choices=sex,null=False)
    birthday            = models.DateField(max_length=10, blank=True, null=True)
    mobile_number	    =models.CharField(max_length=13,blank=True,
                validators = [RegexValidator(regex = CP_NUMBER_REGEX,
                                    message = 'Please enter a valid cellphone number.',
                                    code = 'invalid_cp_number'
                    )]
        )
    image               = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/media/default.jpg'

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="You madee it boii"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )