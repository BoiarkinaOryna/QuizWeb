from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(
        max_length= 255,
        widget = forms.TextInput(attrs={
            "placeholder": "Повідомлення",
            "class": "message-i"
        }),
        label=''
    )