from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(unique=True)
    published_at = models.DateTimeField()
    source_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title