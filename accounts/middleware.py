from typing import TYPE_CHECKING

from django.utils import timezone

from .models import User

if TYPE_CHECKING:
    from typing import Callable

    from django.http import HttpRequest, HttpResponse


class LastSeenMiddleware:
    def __init__(self, get_response: "Callable[[HttpRequest], HttpResponse]") -> None:
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        if not hasattr(request, "user"):
            raise RuntimeError(
                "Middleware error: request has no 'user' attribute. Check middleware order."
            )
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_seen=timezone.now())
        response = self.get_response(request)
        return response
