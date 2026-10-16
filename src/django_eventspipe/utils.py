import json

from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def get_sentinel_user() -> User:
    """
    Prevent pipeline removal when deleting an user
    """
    return get_user_model().objects.get_or_create(username="deleted")[0]

def linkify(field_path: str) -> str:
    """
    Converts a foreign key value or foreign keys of foreign keys into clickable links.
    
    If field_path is 'parent.child', link text will be str(obj.parent.child)
    Link will be the admin url for obj.parent.child.id:change
    """
    def _linkify(obj):
        # Traverse the field path to get the related object
        related_obj = obj
        try:
            for part in field_path.split('.'):
                related_obj = getattr(related_obj, part)
                if related_obj is None:
                    return '-'
        except AttributeError:
            return '-'

        # Build the admin change URL
        app_label = related_obj._meta.app_label
        model_name = related_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[related_obj.pk])

        return format_html('<a href="{}">{}</a>', link_url, related_obj)

    _linkify.short_description = field_path.replace('.', ' -> ')  # Sets column name
    return _linkify

def cronexp(field: str):
    """
    Representation of cron expression.
    """
    return field and field.replace(' ', '') or '*'

# https://stackoverflow.com/a/72256767
class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent: int, sort_keys: bool, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)
