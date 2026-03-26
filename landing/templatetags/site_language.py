from django import template

from landing.site_language import translate_site_message


register = template.Library()


@register.filter
def site_translate(value, lang):
    if value is None:
        return ""
    return translate_site_message(str(value), str(lang))
