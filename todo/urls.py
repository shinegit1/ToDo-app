from django.urls import path
from todo.views import HomePageView, SignupView, AboutPageView, TodoboardView, LogoutView, CreateTodoTaskView, \
    UpdateTodoTaskView, DeleteTodoTaskView
from django.contrib.auth.views import LoginView
from todo.forms import LoginForm

app_name = 'todo'

urlpatterns = [
    path('', HomePageView.as_view(), name='HomePage'),
    path('login/', LoginView.as_view(template_name='registration/login.html', form_class=LoginForm), name='LoginPage'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('signup/', SignupView.as_view(), name='SignupPage'),
    path('todoboard/', TodoboardView.as_view(), name='TodoboardPage'),
    path("create-task/", CreateTodoTaskView.as_view(), name="CreateTodoTask"),
    path("update-task/<int:pk>/", UpdateTodoTaskView.as_view(), name="UpdateTodoTask"),
    path('delete-task/<int:pk>/', DeleteTodoTaskView.as_view(), name="DeleteTodoTask"),
    path('about/', AboutPageView.as_view(), name='AboutPage')
]
