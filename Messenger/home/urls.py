from django.urls import path
from .views import HomePageView, MyPostsView, DeletePostView, UpdatePostView, UpdateProfileView, render_load_image

urlpatterns = [
    path('', view = HomePageView.as_view(), name = 'home'),
    path("my_posts/", view = MyPostsView.as_view(), name = 'my_posts'),
    path("my_posts/<int:pk>/delete/", view = DeletePostView.as_view(), name = 'delete_post'),
    path("my_posts/<int:pk>/change/", view = UpdatePostView.as_view(), name = 'change_post'),
    path("load_image/", view = render_load_image, name = 'load_image'),
    path("edit-profile/<int:pk>", view = UpdateProfileView.as_view(), name = 'edit-profile'),
]