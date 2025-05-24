from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from accounts.models import User

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class Post(models.Model):
    body = models.CharField(max_length=140)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self) -> str:
        return self.body

    @classmethod
    def followed_posts(cls, user: "User") -> "QuerySet[Post]":
        return cls.objects.filter(
            Q(author__in=User.objects.filter(followers=user)) | Q(author=user)
        )
