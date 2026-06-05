from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """Lookup a dictionary value using a key"""
    if dictionary is None:
        return None
    return dictionary.get(key)
