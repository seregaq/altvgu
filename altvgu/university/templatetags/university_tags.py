from django import template
from university.views import cafs_db

register = template.Library()
@register.simple_tag
def get_categories():
    return cafs_db