from django.urls import path
from .views import ChatsView

urlpatterns = [
    path("<int:group_pk>", view = ChatsView.as_view(), name = "chats")
]