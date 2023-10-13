from django.urls import path
from todo.views import HomeView, LoginView, SignupView, AboutView


app_name = 'todo'

urlpatterns = [
    path('', HomeView.as_view(), name = 'Home'),
    path('login/', LoginView.as_view(), name='Login'),
    path('signup/', SignupView.as_view(), name='Signup'),
    path('about/', AboutView.as_view(), name='About')
]
