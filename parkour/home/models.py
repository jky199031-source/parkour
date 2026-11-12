from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel

class HomePage(Page):
    heading = models.CharField("Titre", max_length=200, blank=True)

    content_panels = Page.content_panels + [
            FieldPanel("heading"),
            InlinePanel("sections", label="Sections en escalier"),
        ]

class HomeSection(Orderable):
    page = ParentalKey(
        "HomePage",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    texte = RichTextField("Texte", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image",
    )

    panels = [
        FieldPanel("texte"),
        FieldPanel("image"),
    ]