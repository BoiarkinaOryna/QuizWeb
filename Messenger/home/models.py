from django.db import models
from registration.models import Profile

# Create your models here.

class Image(models.Model):
    filename = models.CharField(max_length = 150)
    file = models.ImageField(upload_to = "images/posts")
    uploaded_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.filename

class Tag(models.Model):
    name = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.name 

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    content = models.TextField(max_length = 4096)
    tags = models.ManyToManyField(Tag, blank = True)
    images = models.ManyToManyField(Image, blank = True, related_name = 'posts_authored')
    views = models.ManyToManyField(Profile, blank = True, related_name = 'posts_viewed')
    likes = models.ManyToManyField(Profile, blank = True, related_name = 'posts_liked')

    def __str__(self):
        return self.title
    
class Link(models.Model):
    url = models.URLField(max_length = 200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    def __str__(self):
        return f'Посилання для поста "{self.post}"'
    
class Avatar(models.Model):
    image = models.ImageField(upload_to = 'images/avatars')
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    active = models.BooleanField(default = True)
    shown = models.BooleanField(default = True)

    def __str__(self):
        return f'Аватар для профілю "{self.profile}"'