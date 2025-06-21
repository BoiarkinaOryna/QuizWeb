from django import forms
from registration.models import Profile, User
from .models import Album

class EditInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "email": "Електронна адреса",
            "password": "Пароль"
        }
        widgets = {
            "first_name": forms.TextInput(attrs = {
                "placeholder": "Lina"
            }),
            "last_name": forms.TextInput(attrs = {
                "placeholder": "Li"
            }),
            "email": forms.TextInput(attrs = {
                "placeholder": "you@example.com"
            }),
            "password": forms.TextInput(attrs = {
                "placeholder": "⁕⁕⁕⁕⁕⁕⁕⁕⁕⁕"
            })
        }
        error_messages = {
            'date_of_birth': {
                'invalid': 'Ця дата не є валідною. Спробуйте формат 2000-01-01'
            }
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["name", "topic"]
        labels = {
            "name": "Назва альбому",
            "theme": "Оберіть тему",
            "year": "Рік альбому"
        }
        widgets = {
            "name": forms.TextInput(attrs = {
                "placeholder": "Настрій"
            }),
            "theme": forms.TextInput(attrs = {
                "placeholder": "Природа"
            }),
            "year": forms.NumberInput(attrs = {
                "placeholder": "Оберіть рік"
            })
        }