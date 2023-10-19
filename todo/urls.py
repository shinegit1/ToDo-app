from django.urls import path
from todo.views import HomeView, SignupView, AboutView, TodoboardView, LogoutView
from django.contrib.auth.views import LoginView
from todo.forms import LoginForm

app_name = 'todo'

urlpatterns = [
    path('', HomeView.as_view(), name = 'HomePage'),
    path('login/', LoginView.as_view(template_name='registration/login.html', form_class=LoginForm), name='LoginPage'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('signup/', SignupView.as_view(), name='SignupPage'),
    path('todoboard/', TodoboardView.as_view(), name='TodoboardPage'),
    path('about/', AboutView.as_view(), name='AboutPage')
]
