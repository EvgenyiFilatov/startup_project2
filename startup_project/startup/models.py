from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """CustomUser extends Django's AbstractUser."""

    first_name = models.CharField('First name', max_length=30)
    last_name = models.CharField('Last name', max_length=30)
    email = models.EmailField('Email', unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Startup(models.Model):
    """
    Represents a startup with a name, description, creator, and developers.
    """
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    creator = models.ForeignKey(
        CustomUser,
        verbose_name='Creator',
        related_name='created_startups',
        on_delete=models.CASCADE
    )
    developers = models.ManyToManyField(
        CustomUser,
        verbose_name='Developers',
        related_name='developer_startups',
        blank=True,
        through='StartupDeveloper',
    )

    def str(self):
        return self.name


class StartupDeveloper(models.Model):

    ROLECHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('builder', 'Builder'),
    ]

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(
        'Role',
        max_length=10,
        choices=ROLECHOICES,
        default='builder'
    )

    def __str__(self):
        return f"{self.user} - {self.get_role_display()} @ {self.startup}"
