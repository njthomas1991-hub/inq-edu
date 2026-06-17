from django import template

from core.models import Avatar

register = template.Library()


@register.filter
def get_user_avatar(user):
    if not getattr(user, "is_authenticated", False):
        return None

    return Avatar.objects.filter(user=user).first()