from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
)
from wagtail.models import Orderable, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from coderedcms.models.snippet_models import Navbar, Footer


@register_setting(icon="cr-desktop", name="crx-settings-override")
class LayoutSettingsOverride(ClusterableModel, BaseSiteSetting):
    """
    Branding, navbar, and theme settings.
    """

    class Meta:
        verbose_name = _("CRX Settings Overrides")

    panels = [
        InlinePanel(
            "site_navbar",
            help_text=_("Choose one or more navbars for your site."),
            heading=_("Site Navbars"),
        ),
        InlinePanel(
            "site_footer",
            help_text=_("Choose one or more footers for your site."),
            heading=_("Site Footers"),
        ),
    ]

@register_snippet
class TranslatableNavbar(Navbar, TranslatableMixin):
    class Meta:
        verbose_name = _("Translatable Navigation Bar")
        verbose_name_plural = _("Translatable Navigation Bars")
        unique_together = (("translation_key", "locale"))

@register_snippet
class TranslatableFooter(Footer, TranslatableMixin):
    class Meta:
        verbose_name = _("Translatable Footer")
        verbose_name_plural = _("Translatable Footers")
        unique_together = (("translation_key", "locale"))

class NavbarOrderableOverride(Orderable, models.Model):
    navbar_chooser = ParentalKey(
        LayoutSettingsOverride,
        related_name="site_navbar",
        verbose_name=_("Site Navbars"),
    )
    navbar = models.ForeignKey(
        TranslatableNavbar,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("navbar")]

class FooterOrderableOverride(Orderable, models.Model):
    footer_chooser = ParentalKey(
        LayoutSettingsOverride,
        related_name="site_footer",
        verbose_name=_("Site Footers"),
    )
    footer = models.ForeignKey(
        TranslatableFooter,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("footer")]
