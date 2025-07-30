from django.db import models
from django.conf import settings

class SearchHistory(models.Model):
    city = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    request_data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Search Histories"

    def __str__(self):
        return f"{self.city} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"