from django.db import models
from django.contrib.postgres.fields import JSONField

class QueryLog(models.Model):
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tone = models.CharField(max_length=100)
    intent = models.CharField(max_length=100)
    suggested_actions = JSONField()
