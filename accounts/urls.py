from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="login.html",
            redirect_authenticated_user=True,
            extra_context={"title": "Sign In"},
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="email/password_reset.txt",
            html_email_template_name="email/password_reset.html",
            subject_template_name="email/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html",
            extra_context={"title": "Reset Password"},
        ),
        name="password_reset_done",
    ),
    path(
        "password/reset/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("register/", views.register, name="register"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("unfollow/<str:username>/", views.unfollow, name="unfollow"),
]
