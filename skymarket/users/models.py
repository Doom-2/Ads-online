from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles:
    ADMIN = "admin"
    USER = "user"
    ROLES = [
        (ADMIN, "Администратор"),
        (USER, "Пользователь"),
    ]


class User(AbstractBaseUser):
    first_name = models.CharField(help_text=_('String from 3 to 64 chars'), max_length=64,
                                  validators=[MinLengthValidator(3)])
    last_name = models.CharField(help_text=_('String from 3 to 64 chars'), max_length=64,
                                 validators=[MinLengthValidator(3)])
    email = models.EmailField(help_text=_('E-mail in valid format'), unique=True)
    role = models.CharField(max_length=10, choices=UserRoles.ROLES, default="user")
    phone = PhoneNumberField(help_text=_('+7(___)___-__-__'), max_length=12, )
    image = models.ImageField(upload_to='user_avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    objects = UserManager()
