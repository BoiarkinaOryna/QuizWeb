from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from registration.models import Profile, User
from home.models import Post
from .models import Friendship
from django.db.models import Q
from django.http import JsonResponse, HttpRequest

# Create your views here.

class FriendsView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = "friends/friends.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'main'

        current_user = Profile.objects.get(user_id = self.request.user).id
        friendships = Friendship.objects.filter(Q(profile2_id=current_user), accepted=False)

        users = []
        for friendship in friendships:
            users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id).id)
        context["requests"] = User.objects.filter(id__in = users)

        friendships = Friendship.objects.filter(Q(profile1_id=current_user) | Q(profile2_id=current_user))
        print("friendships =", friendships)

        friends = []
        for friendship in friendships:
            if friendship.profile1_id == current_user:
                friends.append(User.objects.get(id = Profile.objects.get(id = friendship.profile2_id).user_id).id)
            else:
                friends.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id).id)
           

        context["recommendations"] = User.objects.exclude(id = self.request.user.id).exclude(id__in = friends)

        print("user =", current_user)
        friendships = Friendship.objects.filter(Q(profile1_id=current_user) | Q(profile2_id=current_user), accepted=True)
        print("friendships =", friendships)

        users = []
        for friendship in friendships:
            if friendship.profile1_id == current_user:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile2_id).user_id))
            else:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id))
            print("users =", users)
        context["all_friends"] = users

        return context

class FriendPageView(LoginRequiredMixin, ListView):
    template_name = 'friends/user_prof.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        print("Отриманий user_id:", user_id)
        context["user"] = User.objects.get(id = user_id)
        return context
    
    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return Post.objects.filter(author_id = user_id)


class RequestsView(LoginRequiredMixin, ListView):
    template_name = "friends/friends.html"
    context_object_name = "all_users"

    def get_queryset(self):
        user = Profile.objects.get(user_id = self.request.user)
        friendships = Friendship.objects.filter(Q(profile2_id=user), accepted=False)

        users = []
        for friendship in friendships:
            users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id).id)
            print("users =", users)
        return User.objects.filter(id__in = users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'requests'
        return context
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        print("user1 =", user_id, "user2 =", request.user.id)
        friend_request = Friendship.objects.filter(profile1_id = user_id, profile2_id = request.user.id).first()
        print("friend_request =", friend_request)
        friend_request.accepted = 1
        friend_request.save()

        return JsonResponse({"users": self.queryset})
    
class RecommendationsView(LoginRequiredMixin, ListView):
    template_name = "friends/friends.html"
    context_object_name = "all_users"

    def get_queryset(self):
        current_user = Profile.objects.get(user_id = self.request.user).id
        print("user =", current_user)
        friendships = Friendship.objects.filter(Q(profile1_id=current_user) | Q(profile2_id=current_user))
        print("friendships =", friendships)

        friends = []
        for friendship in friendships:
            if friendship.profile1_id == current_user:
                friends.append(User.objects.get(id = Profile.objects.get(id = friendship.profile2_id).user_id).id)
            else:
                friends.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id).id)
            print("users =", friends)
        return User.objects.exclude(id = self.request.user.id).exclude(id__in = friends)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'recommendations'
        return context
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        friend_request = Friendship.objects.create(
            profile1_id = request.user.id,
            profile2_id = user_id
        )
        friend_request.save()

        return JsonResponse({"users": self.queryset})

class AllFriendsView(LoginRequiredMixin, ListView):
    template_name = "friends/friends.html"
    context_object_name = "all_users"

    def get_queryset(self):
        user = Profile.objects.get(user_id = self.request.user)
        print("user =", user)
        friendships = Friendship.objects.filter(Q(profile1_id=user) | Q(profile2_id=user), accepted=True)
        print("friendships =", friendships)

        users = []
        for friendship in friendships:
            if friendship.profile1_id == user:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile2_id).user_id).id)
            else:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id).id)
            print("users =", users)
        return User.objects.filter(id__in = users)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'all_friends'
        return context
    

def render_delete(request: HttpRequest):
    user_id = request.POST.get("user_id")
    freindship = Friendship.objects.filter(Q(profile1_id = user_id) | Q(profile2_id = user_id)).filter(Q(profile1_id = request.user.id) | Q(profile2_id = request.user.id)).first()
    freindship.delete()
    return JsonResponse({"delete": True})