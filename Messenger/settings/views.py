from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from .forms import EditInfoForm
from home.models import Image
from .models import Album
from registration.models import Profile
from .forms import AlbumForm
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse

# Create your views here.

class PersonalInfoView(UpdateView):
    template_name = "info/info.html"
    form_class = EditInfoForm
    model = Profile
    # fields = ['first_name', 'last_name', 'birthday', 'email', 'password']
    def get_success_url(self):
        return reverse('info', kwargs={'pk': self.object.pk})

class AlbumsView(FormMixin, ListView):
    template_name = "albums/albums.html"
    model = Album
    form_class = AlbumForm
    context_object_name = 'albums'
    
    def get_success_url(self):
        return reverse('albums', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        album = form.save(commit=False)
        # album.author = Album.objects.get(id=self.request.user.id)
        album.save()
        # form.save_m2m()
        return redirect(f"/settings/{self.request.user.id}/albums")
    
def render_save_album_image(requset: HttpRequest):
    image_file = requset.FILES.get("image")
    image = Image.objects.create(
        filename = image_file.name,
        file = image_file
    )
    image.save()

    album_name = requset.POST.get('albumName')
    print("album_name =", album_name)
    album = Album.objects.get(name = album_name)
    album.images.add(image)

    album.save()

    return HttpResponse("loaded")