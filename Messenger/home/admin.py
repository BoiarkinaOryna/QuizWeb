from django.contrib import admin
from .models import Post, Tag, Image

# Register your models here.

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Image)