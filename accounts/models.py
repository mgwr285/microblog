from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. Enter a valid email address."),
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    about_me = models.CharField(max_length=140, blank=True)
    last_seen = models.DateTimeField(default=timezone.now)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )

    def is_following(self, user: "User") -> bool:
        return self.following.filter(pk=user.pk).exists()

    def follow(self, user: "User") -> None:
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user: "User") -> None:
        if self.is_following(user):
            self.following.remove(user)

    def following_count(self) -> int:
        return self.following.count()

    def followers_count(self) -> int:
        return self.followers.count()
