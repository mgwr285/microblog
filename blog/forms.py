from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "cols": 32}),
        }
        labels = {
            "body": _("Say something"),
        }
