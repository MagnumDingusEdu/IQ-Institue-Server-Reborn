from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Student


@receiver(post_save, sender=User)
def create_student_model(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    else:
        instance.student.save()


