from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditProfileForm, UserCreationForm
from .models import User

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    class AuthenticatedHttpRequest(HttpRequest):
        user: User


def register(request: "HttpRequest") -> "HttpResponse":
    if request.user.is_authenticated:
        return redirect("blog:index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations, you are now a registered user!")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"title": "Register", "form": form})


@login_required
def edit_profile(request: "AuthenticatedHttpRequest") -> "HttpResponse":
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your changes have been saved")
            return redirect("accounts:edit_profile")
    else:
        form = EditProfileForm(instance=user)
    return render(request, "edit_profile.html", {"title": "Edit Profile", "form": form})


@login_required
def follow(request: "AuthenticatedHttpRequest", username: str) -> "HttpResponse":
    if request.method != "POST":
        return redirect("blog:index")
    user = get_object_or_404(User, username=username)
    if user == request.user:
        messages.warning(request, "You cannot follow yourself!")
    else:
        request.user.follow(user)
        messages.success(request, f"You are now following {username}!")
    return redirect("blog:user", username=username)


@login_required
def unfollow(request: "AuthenticatedHttpRequest", username: str) -> "HttpResponse":
    if request.method != "POST":
        return redirect("blog:index")
    user = get_object_or_404(User, username=username)
    if user == request.user:
        messages.warning(request, "You cannot unfollow yourself!")
    else:
        request.user.unfollow(user)
        messages.success(request, f"You are no longer following {username}.")
    return redirect("blog:user", username=username)
