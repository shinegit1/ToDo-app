from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from todo.forms import UserSignupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout, authenticate, login


# home Views
class HomeView(TemplateView):
    template_name = 'todo/home.html'


class SignupView(CreateView, SuccessMessageMixin):
    template_name = 'registration/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('todo:TodoboardPage')
    success_message = "Your account registered successfully."

    def form_valid(self, form):
        response = super().form_valid(form)  # We are using create view, and it automatically saves the data
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        if username is not None and password:
            try:
                user = authenticate(username=username, password=password)
                login(self.request, user)
            except Exception:
                raise Exception("Your details is incorrect. Please enter correct details.")
        return response


class LogoutView(LoginRequiredMixin, RedirectView, SuccessMessageMixin):
    """
    A view that logout user and redirect to homepage.
    """
    permanent = True
    query_string = False
    url = reverse_lazy('todo:HomePage')
    success_message = "You are logged out successfully"

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
    

# Todo Task views
class TodoboardView(TemplateView, LoginRequiredMixin):
    template_name = 'todo/todoboard.html'

class AboutView(TemplateView):
    template_name = 'todo/about.html'
