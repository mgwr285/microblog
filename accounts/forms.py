from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as UserChangeForm_,
    UserCreationForm as UserCreationForm_,
    UsernameField,
)

from .models import User


class UserChangeForm(UserChangeForm_):
    class Meta:
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField}


class UserCreationForm(UserCreationForm_):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "about_me")
        widgets = {
            "about_me": forms.Textarea(attrs={"rows": 5, "cols": 40}),
        }
