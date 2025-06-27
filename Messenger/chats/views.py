from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.loader import render_to_string

from .forms import MessageForm
from .models import ChatGroup, ChatMessage
from friends.models import Friendship
from home.models import Profile


class ChatsView(LoginRequiredMixin, FormView):
    template_name = 'chats/chat.html'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_profile = Profile.objects.get(user=self.request.user)
        users_groups = ChatGroup.objects.filter(members=current_profile, is_personal_chat=0)
        context["users_groups"] = users_groups

        group_pk = self.request.POST.get("group_id") or self.request.GET.get("group_id")
        print("POST data:", self.request.POST, self.request.GET)
        print("group_pk", group_pk)
        if group_pk:
            chat_group = ChatGroup.objects.get(pk=group_pk)
            context['chat_group'] = chat_group
            context['message_history'] = ChatMessage.objects.filter(chat_group=chat_group)

        current_user = Profile.objects.get(user_id = self.request.user).id
        friendships = Friendship.objects.filter(Q(profile1_id=current_user) | Q(profile2_id=current_user), accepted=True)
        users = []
        for friendship in friendships:
            if friendship.profile1_id == current_user:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile2_id).user_id))
            else:
                users.append(User.objects.get(id = Profile.objects.get(id = friendship.profile1_id).user_id))
            print("users =", users)
        context["all_friends"] = users
        return context

    def form_valid(self, form):
        group_pk = self.request.POST.get("group_id")
        if not group_pk:
            return HttpResponseForbidden("Missing group ID")

        try:
            chat_group = ChatGroup.objects.get(pk=group_pk)
        except ChatGroup.DoesNotExist:
            return HttpResponseForbidden("Chat group not found")

        current_profile = Profile.objects.get(user=self.request.user)

        if current_profile not in chat_group.members.all():
            return HttpResponseForbidden('<h1>У Вас немає доступу до цього чату</h1>')

        message = form.save(commit=False)
        message.author = current_profile
        message.chat_group = chat_group
        message.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        group_pk = self.request.POST.get("group_id")
        if not group_pk:
            return HttpResponseForbidden("Missing group ID")

        try:
            chat_group = ChatGroup.objects.get(pk=group_pk)
        except ChatGroup.DoesNotExist:
            return HttpResponseForbidden("Chat group not found")
        # if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "chats/chat_block.html",
            context = {
                "form": form,
                "chat_group": chat_group,
                "message_history": ChatMessage.objects.filter(chat_group=chat_group),
            },
            request=self.request,
        )
        return HttpResponse(html)