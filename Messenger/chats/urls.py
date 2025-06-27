from django.urls import path
from .views import ChatsView

urlpatterns = [
    path("", view = ChatsView.as_view(), name = "chats")
]