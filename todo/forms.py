from django import forms
from todo.models import CustomUser, TodoTask
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import enum


# User login forms here.
class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'eg: example@gmail.com'}),
        error_messages={'required': 'Required. Please enter your email ID'})
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}),
        strip=False, error_messages={'required': 'Required. Please enter your password'})


# User sign up form here
class UserSignupForm(UserCreationForm):
    """
        This form is used to create a new account for the user.
        """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Type unique password'}),
                                strip=False, error_messages={'required': 'Required. Please create password'})
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Re-type the password'}),
                                strip=False, error_messages={'required': 'Required. Please re-enter the password'})

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eg: example@gmail.com'}),
        }
        error_messages = {
            'email': {'required': 'Required. Please enter your email ID'}
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            self.add_error("email", _("Error: A user with this email already exists."))
        return email


class TodoTaskStatus(enum.Enum):
    SELECT = 'Select Option'
    INPROGRESS = 'In-Progress'
    COMPLETED = 'Complete'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['description', 'status', 'end_date', 'time']
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter a brief detail about the task', 'rows': "6"}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=TodoTaskStatus.choices()),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
        }
        error_messages = {
            'description': {'required': 'Required. Please enter description'},
            'end_date': {'required': "Required. Please select date"},
            'status': {'required': "Required. Please select an option"},
            'time': {'required': "Required. Please select time"}
        }
