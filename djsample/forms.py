from django import forms
from djsample.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_teacher' )

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['username'].widget.attrs['class'] = 'form-control'
      self.fields['password1'].widget.attrs['class'] = 'form-control'
      self.fields['password2'].widget.attrs['class'] = 'form-control'
      self.fields['is_teacher'].widget.attrs['class'] = 'form-check-input'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
