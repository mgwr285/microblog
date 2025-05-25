from typing import TYPE_CHECKING

from django import template
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
    from datetime import datetime

register = template.Library()


@register.simple_tag
def include_dayjs() -> str:
    return mark_safe(
        """
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/dayjs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/plugin/localizedFormat.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/plugin/relativeTime.js"></script>
    <script>
    dayjs.extend(dayjs_plugin_localizedFormat);
    dayjs.extend(dayjs_plugin_relativeTime);

    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('[data-dayjs="from-now"]').forEach(element => {
            element.textContent = dayjs(element.dataset.timestamp).fromNow();
        });
        
        document.querySelectorAll('[data-dayjs="format"]').forEach(element => {
            const format = element.dataset.format || 'LLL';
            element.textContent = dayjs(element.dataset.timestamp).format(format);
        });
    });
    </script>
    """
    )


@register.simple_tag
def dayjs_format(dt: "datetime", format: str = "LLL") -> str:
    if not dt:
        return ""
    isoformat = dt.isoformat()
    return mark_safe(
        f'<span data-dayjs="format" data-timestamp="{isoformat}" data-format="{format}"></span>'
    )


@register.simple_tag
def dayjs_from_now(dt: "datetime") -> str:
    if not dt:
        return ""
    isoformat = dt.isoformat()
    return mark_safe(
        f'<span data-dayjs="from-now" data-timestamp="{isoformat}"></span>'
    )
