from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Project

@receiver(pre_delete, sender=Project)
def send_rejection_email_on_delete(sender, instance, **kwargs):
    """
    Wysyła e-mail do użytkownika, gdy jego projekt jest usuwany.
    Działa zarówno przy usuwaniu pojedynczym, jak i masowym.
    """
    # Sprawdź, czy projekt nie był zatwierdzony i czy użytkownik podał e-mail
    if not instance.is_approved and instance.user_email:
        try:
            subject = f'Twój projekt "{instance.title}" został odrzucony'
            message = (
                f'Cześć,\n\n'
                f'informujemy, że Twój projekt "{instance.title}" został usunięty z naszej bazy, '
                f'ponieważ nie spełniał on wymogów regulaminu Banku Pomysłów.\n\n'
                f'Jeśli masz pytania lub chcesz dowiedzieć się więcej, skontaktuj się z nami.\n\n'
                f'Pozdrawiamy\n'
                f'Zespół Banku Pomysłów'
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.user_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Błąd podczas wysyłania e-maila o usunięciu projektu: {e}")