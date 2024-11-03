from django.db import models
from django.contrib.auth.models import User

class UserProfileREADME(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="")  # Markdown content
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s README"
