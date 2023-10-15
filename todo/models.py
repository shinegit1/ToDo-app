from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.urls import reverse_lazy
import enum
from django.contrib.auth.validators import ASCIIUsernameValidator


# Create your models here.
class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(_("username"),
                                max_length=150,
                                unique=True,
                                help_text=_("Required. letters, digits and @/./+/-/_ only."),
                                validators=[username_validator],
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                }, )
    email = models.EmailField(_("email address"),
                              unique=True,
                              error_messages={
                                  "unique": _("A user with that email address already exists."),
                              }, )

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email).lower()
        super().clean()



class TodoTaskStatus(enum.Enum):
    ASSIGNED = 'ASSIGNED'
    COMPLETED = 'COMPLETED'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TodoTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_index=True)
    submitted_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TodoTaskStatus.choices())
