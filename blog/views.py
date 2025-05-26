from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from .forms import PostForm
from .models import Post

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from accounts.models import User as UserModel

    class AuthenticatedHttpRequest(HttpRequest):
        user: UserModel


User = get_user_model()


@login_required
def index(request: "AuthenticatedHttpRequest") -> "HttpResponse":
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, _("Your post is now live!"))
            return redirect("blog:index")
    else:
        form = PostForm()
    paginator = Paginator(
        Post.followed_posts(request.user),
        getattr(settings, "POSTS_PER_PAGE", 25),
    )
    page = request.GET.get("page", "1")
    posts = paginator.get_page(page)
    prev_url = (
        reverse("blog:index") + f"?page={posts.previous_page_number()}"
        if posts.has_previous()
        else None
    )
    next_url = (
        reverse("blog:index") + f"?page={posts.next_page_number()}"
        if posts.has_next()
        else None
    )
    return render(
        request,
        "index.html",
        {
            "title": _("Home"),
            "form": form,
            "posts": posts,
            "prev_url": prev_url,
            "next_url": next_url,
        },
    )


@login_required
def explore(request: "AuthenticatedHttpRequest") -> "HttpResponse":
    page = request.GET.get("page", "1")
    paginator = Paginator(
        Post.objects.all(),
        getattr(settings, "POSTS_PER_PAGE", 25),
    )
    posts = paginator.get_page(page)
    prev_url = (
        reverse("blog:explore") + f"?page={posts.previous_page_number()}"
        if posts.has_previous()
        else None
    )
    next_url = (
        reverse("blog:explore") + f"?page={posts.next_page_number()}"
        if posts.has_next()
        else None
    )
    return render(
        request,
        "index.html",
        {
            "title": _("Explore"),
            "posts": posts,
            "prev_url": prev_url,
            "next_url": next_url,
        },
    )


@login_required
def user(request: "AuthenticatedHttpRequest", username: str) -> "HttpResponse":
    user = get_object_or_404(User, username=username)
    paginator = Paginator(
        Post.objects.filter(author=user),
        getattr(settings, "POSTS_PER_PAGE", 25),
    )
    page = request.GET.get("page", "1")
    posts = paginator.get_page(page)
    prev_url = (
        reverse("blog:user", kwargs={"username": user.username})
        + f"?page={posts.previous_page_number()}"
        if posts.has_previous()
        else None
    )
    next_url = (
        reverse("blog:user", kwargs={"username": user.username})
        + f"?page={posts.next_page_number()}"
        if posts.has_next()
        else None
    )
    return render(
        request,
        "user.html",
        {
            "user_": user,
            "following": request.user.is_following(user),
            "posts": posts,
            "prev_url": prev_url,
            "next_url": next_url,
        },
    )
