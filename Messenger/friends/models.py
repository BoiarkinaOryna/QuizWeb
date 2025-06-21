from django.db import models
from registration.models import Profile

# Create your models here.
class Friendship(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'friendship_sent_request')
    profile2 = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'friendship_accepted_request')
    accepted = models.BooleanField(default = False)