from django.db import models
from django.contrib.auth.models import User

class Paste(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Paste by {self.user.username} (expires {self.expires_at})"
