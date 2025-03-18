from django import template

register = template.Library()

@register.simple_tag
def get_schedule(group_id):
    schedule = ["ОЛКК", "АЛГЕМ", "ТИМП"]

    if group_id > 10:
        schedule = list(reversed(schedule))  # Преобразуем в список

    return schedule
