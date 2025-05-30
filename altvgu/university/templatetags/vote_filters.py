from django import template

register = template.Library()

@register.filter
def likes_count(votes):
    return votes.filter(value=1).count()

@register.filter
def dislikes_count(votes):
    return votes.filter(value=-1).count()
