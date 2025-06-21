import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.views import LogoutView


from .forms import UserForm, AuthUserForm
from .models import User

def generate_code():
    str_code = ''
    for num in range(6):
        random_num = random.randint(0,9)
        str_code += str(random_num)

    return str_code

# Create your views here.

class RegistrationPageView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.save()
        password1 = form.cleaned_data['password']
        password2 = form.cleaned_data['password_confirmation']
        if password1 == password2:
            code = generate_code()
            user_email = form.cleaned_data['email']
            self.request.session['confirmation_code'] = code
            self.request.session['user_data'] = form.cleaned_data

            send_mail(
                "Код підтвердження",
                f"Добрий день! Ось Ваш код підтвердження: \n {code}",
                "boyarkina.ar@gmail.com",
                [f"{user_email}"],
                fail_silently=False,
            )
            return redirect("/registration/validation")
        else:
            return redirect("/registration")

def validation_view(request: HttpRequest):
    if request.method == "POST":
        input_code = request.POST.get("code")
        real_code = request.session.get("confirmation_code")

        if input_code == real_code:
            data = request.session.get("user_data")
            user = User.objects.create(
                email=data['email'],
                password=data['password'],
            )
            request.session.pop('confirmation_code', None)
            request.session.pop('user_data', None)

        
        return redirect('/registration/authorization')
    return render(
        request = request,
        template_name = 'validation/validation.html',
    )

def authorization_page(request: HttpRequest):
    form = AuthUserForm()
    password_error = False
    existance_error = False
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            profile = User.objects.filter(email = email)[0]
            if password == profile.password:
                login(request = request, user = profile)
                return redirect('/')
            else:
                password_error = True
        except:
            existance_error = True

    return render(
        request = request,
        template_name = 'authorization/authorization.html',
        context = {
            'form': form,
            "password_error": password_error,
            "existance_error": existance_error
        }
    )

class CustomLogoutView(LogoutView):
    next_page = 'authorization'