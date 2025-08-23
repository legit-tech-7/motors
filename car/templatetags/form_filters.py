from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if not isinstance(field, BoundField):
        return field  # return it as-is if it's not a form field
    return field.as_widget(attrs={'class': css_class})
