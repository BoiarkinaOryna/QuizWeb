from .views import RegistrationPageView, authorization_page, validation_view, CustomLogoutView
# from .views import AuthorizationPageView
from django.urls import path

urlpatterns = [
    path('', view = RegistrationPageView.as_view(), name = 'registration'),
    path('authorization', view = authorization_page, name = 'authorization'),
    path('validation', view = validation_view, name = "validation"),
    path('logout', view = CustomLogoutView.as_view(), name = 'logout')
]