from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.generic import ListView, FormView
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db.models import F

from .forms import MessageForm
from .models import ChatGroup, ChatMessage
from home.models import Profile

class ChatsView(FormView):
    template_name = 'chats/chat.html'
    form_class = MessageForm
    
    def dispatch(self, request, *args, **kwargs):
        '''Метод dispatch обробляє GET та POST запити'''
        # Отримуємо group_pk з нашого url
        group_pk = self.kwargs['group_pk']
        #Отримуємо chat_group з модели
        chat_group = ChatGroup.objects.get(pk = group_pk)
        #Перевіряемо чи є такий користувач у списку учасників групи
        print(chat_group.members.all(), Profile.objects.get(user_id = request.user.id))
        if Profile.objects.get(user_id = request.user.id) not in chat_group.members.all():
            #Якщо користувача не має видаємо помилку
            return HttpResponseForbidden('<h1>У Вас немає доступу до цього чату</h1>')
        # Оброблюємо запит 
        for message in ChatMessage.objects.filter(chat_group = chat_group):
            # message.sent_at = message.sent_at.isoformat()
            message.save()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''
        У методі ми перадаємо інформацію про групу чата
        '''
        #отримуємо дані і зберігаємо їх в context
        context =  super().get_context_data(**kwargs) 
        #отримуємо group
        group_pk = self.kwargs['group_pk']
        #
        context['chat_group'] = ChatGroup.objects.get(pk = group_pk)
        #
        context['message_history'] = ChatMessage.objects.filter(chat_group_id = group_pk)
        print("context =", context)
        return context