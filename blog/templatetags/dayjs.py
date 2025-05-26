from typing import TYPE_CHECKING

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

if TYPE_CHECKING:
    from datetime import datetime

register = template.Library()


@register.simple_tag
def include_dayjs() -> str:
    current_lang = get_language() or "en"
    dayjs_locale = current_lang.split("-")[0]

    return mark_safe(
        f"""
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/dayjs.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/plugin/localizedFormat.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1.11.13/plugin/relativeTime.js"></script>
    <script>
    dayjs.extend(dayjs_plugin_localizedFormat);
    dayjs.extend(dayjs_plugin_relativeTime);

    if ('{dayjs_locale}' !== 'en') {{
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/dayjs@1.11.13/locale/{dayjs_locale}.js';
        script.onload = function () {{
            dayjs.locale('{dayjs_locale}');
            initializeDayjs();
        }};
        script.onerror = function () {{
            console.warn('Day.js locale {dayjs_locale} not found, using English');
            initializeDayjs();
        }};
        document.body.appendChild(script);
    }} else {{
        initializeDayjs();
    }}

    function initializeDayjs() {{
        document.querySelectorAll('[data-dayjs="from-now"]').forEach(element => {{
            element.textContent = dayjs(element.dataset.timestamp).fromNow();
        }});
        
        document.querySelectorAll('[data-dayjs="format"]').forEach(element => {{
            const format = element.dataset.format || 'LLL';
            element.textContent = dayjs(element.dataset.timestamp).format(format);
        }});
    }}
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
