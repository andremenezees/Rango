from django import template

from pypro.rango.models import Categoria

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list():
    return {'cats': Categoria.objects.all()}
