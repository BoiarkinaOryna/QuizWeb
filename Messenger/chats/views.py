from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.template.loader import render_to_string

from .forms import MessageForm, NewGroupForm
from .models import ChatGroup, ChatMessage
from home.models import Profile


class ChatsView(LoginRequiredMixin, FormView):
    template_name = 'chats/chat.html'
    form_class = NewGroupForm

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
        html = render_to_string(
            "chats/chat_block.html",
            {
                "chat_group": chat_group,
                "message_history": ChatMessage.objects.filter(chat_group=chat_group),
            },
            request=self.request
        )
        return HttpResponse(html)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs
    
class CreateGroupView(FormView):
    form_class = NewGroupForm
    template_name = 'chats/chat.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        group = form.save(commit=False)
        group.admin = Profile.objects.get(user_id = User.objects.get(id = self.request.user.id).id)

        group.save()
        form.save_m2m()

        return super().form_valid(form)