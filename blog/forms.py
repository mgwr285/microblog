from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "cols": 32}),
        }
        labels = {
            "body": "Say something",
        }
