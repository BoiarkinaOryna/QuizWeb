from django.urls import path
from .views import FriendsView, FriendPageView, RequestsView, RecommendationsView, AllFriendsView, render_delete

urlpatterns = [
    path("", view = FriendsView.as_view(), name = "friends"),
    path("requests/", view = RequestsView.as_view(), name = "requests"),
    path("recommendations/", view = RecommendationsView.as_view(), name = "recommendations"),
    path("all_friends/", view = AllFriendsView.as_view(), name = "all_friends"),
    path("delete/", view = render_delete, name = "delete"),
    path("friend/<int:pk>", view = FriendPageView.as_view(), name='friend_page')
]