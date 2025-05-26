from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as LoginView_
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import EditProfileForm, UserCreationForm
from .models import User

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpRequest, HttpResponse

    class AuthenticatedHttpRequest(HttpRequest):
        user: User


class LoginView(LoginView_):
    def get(
        self, request: "HttpRequest", *args: "Any", **kwargs: "Any"
    ) -> "HttpResponse":
        if request.GET.get("next"):
            messages.info(request, _("Please log in to access the page."))
        return super().get(request, *args, **kwargs)


def register(request: "HttpRequest") -> "HttpResponse":
    if request.user.is_authenticated:
        return redirect("blog:index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Congratulations, you are now a registered user!")
            )
            return redirect("accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"title": _("Register"), "form": form})


@login_required
def edit_profile(request: "AuthenticatedHttpRequest") -> "HttpResponse":
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your changes have been saved"))
            return redirect("accounts:edit_profile")
    else:
        form = EditProfileForm(instance=user)
    return render(
        request, "edit_profile.html", {"title": _("Edit Profile"), "form": form}
    )


@login_required
def follow(request: "AuthenticatedHttpRequest", username: str) -> "HttpResponse":
    if request.method != "POST":
        return redirect("blog:index")
    user = get_object_or_404(User, username=username)
    if user == request.user:
        messages.warning(request, _("You cannot follow yourself!"))
    else:
        request.user.follow(user)
        messages.success(
            request, _("You are now following %(username)s!") % {"username": username}
        )
    return redirect("blog:user", username=username)


@login_required
def unfollow(request: "AuthenticatedHttpRequest", username: str) -> "HttpResponse":
    if request.method != "POST":
        return redirect("blog:index")
    user = get_object_or_404(User, username=username)
    if user == request.user:
        messages.warning(request, _("You cannot unfollow yourself!"))
    else:
        request.user.unfollow(user)
        messages.success(
            request,
            _("You are no longer following %(username)s.") % {"username": username},
        )
    return redirect("blog:user", username=username)
