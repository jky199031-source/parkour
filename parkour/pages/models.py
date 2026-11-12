from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel,MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet

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
    parkour_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de fond",
    )
    heading = models.CharField("Titre", max_length=200, blank=True)
    body = RichTextField("Actualités du mois", blank=True)
    events_title = models.CharField(
        "Titre de la section événements",
        max_length=100,
        default="Événements",
    )

    content_panels = Page.content_panels + [
        FieldPanel("parkour_image"),
        FieldPanel("heading"),
        FieldPanel("body"),
        FieldPanel("events_title"),
        InlinePanel("evenements", label="Événements")
    ]

class Evenement(Orderable):
    page = ParentalKey(
        "ActivitesPage",
        on_delete=models.CASCADE,
        related_name="evenements",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de fond",
    )
    titre = models.CharField("Titre", max_length=120)
    date = models.CharField("Date et horaire", max_length=100, blank=True)
    texte = RichTextField("Texte", blank=True)
    adresse = models.CharField("Adresse", max_length=250, blank=True)

    panels = [
        FieldPanel("titre"),
        FieldPanel("date"),
        FieldPanel("texte"),
        FieldPanel("adresse"),
        FieldPanel("image"),
    ]

class GaleriePage(Page):
    content_panels = Page.content_panels + [
        InlinePanel("items", label="Photos et vidéos"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        kind = request.GET.get("type", "photo")
        if kind not in ("photo", "video"):
            kind = "photo"

        items = self.items.filter(kind=kind)

        paginator = Paginator(items, 9)
        try:
            page_obj = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj =paginator.page(paginator.num_pages)

        context["kind"] = kind
        context["page_obj"] = page_obj
        return context

class GalerieItem(Orderable):
    page = ParentalKey(
        "GaleriePage",
        on_delete=models.CASCADE,
        related_name="items",
    )
    kind = models.CharField(
        "Type",
        max_length=5,
        choices=[("photo", "Photo"), ("video", "Vidéo")],
        default="photo",
    )
    titre = models.CharField("Légende", max_length=120, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Photo",
    )
    video_url = models.URLField("Lien de la vidéo (YouTube ou Vimeo)", blank=True)

    panels = [
        FieldPanel("kind"),
        FieldPanel("titre"),
        FieldPanel("image"),
        FieldPanel("video_url"),
    ]
class SocialPage(Page):
    pass

@register_snippet
class ReseauSocial(models.Model):
    nom = models.CharField("Nom du réseau", max_length=50)
    url = models.URLField("Adresse de votre profil")
    ordre = models.PositiveIntegerField("Ordre d'affichage", default=0)

    panels = [
        FieldPanel("nom"),
        FieldPanel("url"),
        FieldPanel("ordre"),
    ]

    class Meta:
        ordering = ["ordre", "nom"]
        verbose_name = "réseau social"
        verbose_name_plural = "réseaux sociaux"

    def __str__(self):
        return self.nom

class AboutPage(Page):
    pass

class LegalPage(Page):
    pass

class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(AbstractEmailForm):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image",
    )
    intro = RichTextField("Texte d'introduction", blank=True)
    thank_you_text = RichTextField("Message de remerciement", blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("image"),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel("from_address"),
                    FieldPanel("to_address"),
                ]),
                FieldPanel("subject"),
            ],
            "Envoi par e-mail",
        ),
    ]