from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255, default="default-course")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_active = models.BooleanField(default=True)

    logged_in = models.BooleanField(default=False)
    last_login_time = models.DateTimeField(default=None, blank=True, null=True)
    courses = models.ManyToManyField(Course)
    multi_device_login = models.BooleanField(default=False)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user.username + " - " + self.user.first_name


class NewRegistration(models.Model):
    name = models.CharField(max_length=1024)
    email = models.EmailField()
    courses = models.CharField(max_length=1024)
    mobile = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
