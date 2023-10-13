from django import forms
from todo.models import CustomUser, TodoTask
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


# User login forms here.
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'eg: example@gmail.com'}),
        error_messages={'required': 'Required. Please enter your email ID'})
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Type unique password'}))

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email ID)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                return ValidationError(self.error_messages["invalid_login"], code="invalid_login")
            else:
                if self.user_cache.is_active:
                    raise ValidationError(self.error_messages["inactive"], code="inactive")

        return self.cleaned_data


# User sign up form here
class UserSignupForm(UserCreationForm):
    """
        This form is used to create a new account for the user.
        """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 
                                    'placeholder': 'Type unique password'}), 
                                strip=False)
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control', 
                                    'placeholder': 'Re-type the same password'}),
                                strip= False)
    

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eg: example@gmail.com'}),
        }
        error_messages = {
            'first_name': {'required': 'Required. Please enter your first name'},
            'last_name': {'required': 'Required. Please enter your last name'},
            'email': {'required': 'Required. Please enter your email ID'},
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            self.add_error("email", _("A user with this email already exists."))
        return email


class CreateTodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = []
