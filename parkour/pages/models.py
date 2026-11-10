from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel

class CoursPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel("blocs", label="Blocs du cours"),
    ]
    subpage_types = ["pages.CoursDetailPage"]
   
class CoursBloc(Orderable):
    page = ParentalKey(
        "CoursPage",
        on_delete=models.CASCADE,
        related_name="blocs",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    titre = models.CharField("Titre", max_length=100, blank=True)
    texte = RichTextField("Texte", blank=True)
    cours_page = models.ForeignKey(
        "pages.CoursDetailPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Page du cours",
    )
    lien = models.URLField("Adresse", blank=True)
    texte_lien = models.CharField(
        "Texte du bouton",
        max_length=60,
        default="Rejoindre le cours",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("titre"),
        FieldPanel("texte"),
        FieldPanel("cours_page"),
        FieldPanel("lien"),
        FieldPanel("texte_lien"),
    ]

class CoursDetailPage(Page):
    parent_page_types = ["pages.CoursPage"]
    subpage_types = []

    video_url = models.URLField(
        "Lien de la vidéo (YouTube ou Vimeo)",
        blank=True,
    )
    intro = models.CharField("Résumé", max_length=250, blank=True)
    body = RichTextField("Description", blank=True)
    niveau = models.CharField("Niveau", max_length=100, blank=True)
    horaires = models.CharField("Jours et horaires", max_length=200, blank=True)
    lieu = models.CharField("Lieu", max_length=200, blank=True)
    lien_inscription = models.URLField("Lien d'inscription", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("video_url"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("niveau"),
        FieldPanel("horaires"),
        FieldPanel("lieu"),
        FieldPanel("lien_inscription"),
    ]

class ActivitesPage(Page):
    pass

class GaleriePage(Page):
    pass

class SocialPage(Page):
    pass

class AboutPage(Page):
    pass

class LegalPage(Page):
    pass

class ContactPage(Page):
    pass
