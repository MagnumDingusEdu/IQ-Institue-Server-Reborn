from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from users.models import Student


@receiver(post_save, sender=User)
def create_student_model(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
    else:
        instance.student.save()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'ip_addr': reset_password_token.ip_address
    }

    # render email text
    email_html_message = render_to_string('users/user_reset_password.html', context)
    email_plaintext_message = render_to_string('users/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset for {reset_password_token.user.email}",
        # message:
        email_plaintext_message,
        # from:
        "IQ Institute",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
