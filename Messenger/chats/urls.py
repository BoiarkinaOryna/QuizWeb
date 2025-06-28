from django.urls import path
from .views import ChatsView, CreateGroupView

urlpatterns = [
    path("", view = ChatsView.as_view(), name = "chats"),
    path("create_group/", view = CreateGroupView.as_view(), name = 'create_group')
]