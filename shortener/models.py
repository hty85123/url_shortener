from django.db import models
from django.contrib.auth.models import User

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('original_url', 'user')

    def __str__(self):
        return f"{self.short_url} -> {self.original_url}"

class ClickRecord(models.Model):
    short_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name="clicks")
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.short_url.short_url} from {self.ip_address}"
