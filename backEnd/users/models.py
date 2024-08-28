from django.db import models
from django.contrib.auth.models import User


#User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferential_topics = models.JSONField(default=list, blank=True)  
    read_to_me = models.BooleanField(default=False)
    magnified_text = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username