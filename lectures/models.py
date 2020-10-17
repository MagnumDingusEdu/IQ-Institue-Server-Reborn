from django.db import models
from users.models import Course
import uuid

# Create your models here.

TYPE_CHOICES = [
    ("dir", "Directory"),
    ("vid", "Lecture"),
]


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1024)
    type = models.CharField(choices=TYPE_CHOICES, default="dir", max_length=1024)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    courses = models.ManyToManyField(Course)
    video_link = models.CharField(max_length=512, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    path = models.TextField(default="")

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.path = calculate_path(self)
        super(Node, self).save()


def calculate_path(instance):
    if instance.parent is None:
        return "/"
    return calculate_path(instance.parent) + instance.parent.title + "/"
