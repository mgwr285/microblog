from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import User

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class Post(models.Model):
    body = models.CharField(_("body"), max_length=140)
    timestamp = models.DateTimeField(_("timestamp"), default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("author"),
    )

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self) -> str:
        return self.body

    @classmethod
    def followed_posts(cls, user: "User") -> "QuerySet[Post]":
        return cls.objects.filter(
            Q(author__in=User.objects.filter(followers=user)) | Q(author=user)
        )
