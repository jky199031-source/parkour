from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    parkour_image = models.ForeignKey(
            "wagtailimages.Image",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="+",
            verbose_name="Image de fond",
        )
    heading = models.CharField("Titre", max_length=200, blank=True)
    body = RichTextField("Message d'accueil", blank=True)

    content_panels = Page.content_panels + [
            FieldPanel("parkour_image"),
            FieldPanel("heading"),
            FieldPanel("body"),
        ]
