from django.db import models
from home.models import Image, Tag
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    preview_image = models.ImageField(upload_to = 'images/album_previews', null = True, blank = True)
    images = models.ManyToManyField(Image, blank = True)
    topic = models.ForeignKey(Tag, on_delete = models.CASCADE)
    shown = models.BooleanField(default = True)

    def __str__(self):
        return self.name

