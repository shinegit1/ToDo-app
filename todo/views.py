from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

# home Views
class HomeView(TemplateView):
    template_name = 'todo/home.html'


# Create Views for Authentication
class LoginAPIView(TemplateView):
    template_name ='registration/login.html'


class SignupView(TemplateView):
    template_name = 'registration/signup.html'


class LogoutView(TemplateView):
    pass

# Todo Task views
class TodoboardView(TemplateView, LoginRequiredMixin):
    template_name = 'todo/todoboard.html'

class AboutView(TemplateView):
    template_name = 'todo/about.html'
