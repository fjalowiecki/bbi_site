from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=250)
    org_email = models.EmailField()
    org_phone = models.IntegerField(null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"