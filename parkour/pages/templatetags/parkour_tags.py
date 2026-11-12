from django import template
from pages.models import ReseauSocial

register = template.Library()


@register.simple_tag
def reseaux_sociaux():
    return ReseauSocial.objects.all()