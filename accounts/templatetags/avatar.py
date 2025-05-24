from typing import TYPE_CHECKING

from hashlib import md5

from django import template

if TYPE_CHECKING:
    from ..models import User

register = template.Library()


@register.filter
def avatar(user: "User", size: int = 36) -> str:
    digest = md5(user.email.lower().encode("utf-8"), usedforsecurity=False).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
