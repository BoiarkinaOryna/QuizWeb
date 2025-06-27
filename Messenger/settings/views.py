from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import EditInfoForm
from home.models import Image, Avatar
from .models import Album
from registration.models import Profile, User
from .forms import AlbumForm
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse

# Create your views here.

class PersonalInfoView(LoginRequiredMixin, UpdateView):
    template_name = "info/info.html"
    form_class = EditInfoForm
    model = User
    # fields = ['first_name', 'last_name', 'birthday', 'email', 'password']
    def get_success_url(self):
        return reverse('info', kwargs={'pk': self.object.pk})
    
    # def get_queryset(self):
    #     return User.objects.get(id = self.request.user.id)

class AlbumsView(LoginRequiredMixin, FormMixin, ListView):
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatars"] = Avatar.objects.filter(profile_id = Profile.objects.get(user_id = User.objects.get(id = self.request.user.id).id))
        return context
    
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

def render_save_avatar(request: HttpRequest):
    print("request", User.objects.get(id = request.user.id))
    if request.method == "POST":
        previous_list = Avatar.objects.filter(profile = Profile.objects.get(user_id = User.objects.get(id = request.user.id).id))
        for previous in previous_list:
            previous.active = False

        avatar = Avatar.objects.create(
            image = request.FILES.get("image"),
            profile = Profile.objects.get(user_id = User.objects.get(id = request.user.id).id)
        )
        avatar.save()
    return HttpResponse("loaded")