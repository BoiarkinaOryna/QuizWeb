from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>", view = PersonalInfoView.as_view(), name = "info"),
    path("<int:pk>/albums", view = AlbumsView.as_view(), name = "albums"),
    path("save_album_image", view = render_save_album_image, name = "save"),
    path("save_image", view = render_save_avatar)
]