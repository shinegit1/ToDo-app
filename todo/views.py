from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, RedirectView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from todo.forms import UserSignupForm, TodoTaskForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout, authenticate, login
from todo.models import TodoTask


# home Views
class HomePageView(TemplateView):
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
class TodoboardView(LoginRequiredMixin, ListView, TemplateView):
    template_name = 'todo/todoboard.html'

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        if queryset is None:
            self.object_list = TodoTask.objects.filter(user=self.request.user)
        ...
        return super().get_context_data(**kwargs)


class CreateTodoTaskView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TodoTask
    template_name = 'todo/task_form.html'
    form_class = TodoTaskForm
    success_url = reverse_lazy('todo:TodoboardPage')
    success_message = "Your task is created successfully"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateTodoTaskView, self).form_valid(form)


class UpdateTodoTaskView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    template_name = 'todo/task_form.html'
    model = TodoTask
    form_class = TodoTaskForm
    success_url = reverse_lazy('todo:TodoboardPage')
    success_message = "Your task updated successfully"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["task"] = TodoTask.objects.get(id=self.kwargs['pk'])
        return context


class DeleteTodoTaskView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TodoTask
    success_url = reverse_lazy('todo:TodoboardPage')
    success_message = "Your task deleted successfully"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AboutPageView(TemplateView):
    template_name = 'todo/about.html'
