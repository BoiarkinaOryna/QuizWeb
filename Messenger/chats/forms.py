from django import forms
from registration.models import Profile
from .models import ChatGroup


class MessageForm(forms.Form):
    message = forms.CharField(
        max_length= 255,
        widget = forms.TextInput(attrs={
            "placeholder": "Повідомлення",
            "class": "message-i"
        }),
        label=''
    )

class NewGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = Profile.objects.exclude(id=current_user.id)
    users = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.exclude(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'tag-div'
        }),
        label = '',
        required = False,
    )
    class Meta:
        model = ChatGroup
        fields = ['name', 'avatar']