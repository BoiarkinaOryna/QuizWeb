from django.db import models
from home.models import Image, Tag
from registration.models import Profile
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    preview_image = models.ImageField(upload_to = 'images/album_previews', null = True, blank = True)
    images = models.ManyToManyField(Image, blank = True)
    topic = models.ForeignKey(Tag, on_delete = models.CASCADE)
    shown = models.BooleanField(default = True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

