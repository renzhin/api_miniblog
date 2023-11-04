from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_email(user, message):
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject=message,
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.AUTH_EMAIL,
        recipient_list=(user.email,),
        fail_silently=False,
    )
