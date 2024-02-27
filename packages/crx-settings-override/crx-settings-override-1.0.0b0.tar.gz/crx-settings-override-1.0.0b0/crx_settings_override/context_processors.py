from coderedcms.templatetags.coderedcms_tags import get_navbars, get_footers

from crx_settings_override.models import LayoutSettingsOverride, TranslatableNavbar, TranslatableFooter

def navbars(request):
    layout = LayoutSettingsOverride.for_request(request)
    navbarorderables = layout.site_navbar.all()
    navbars = TranslatableNavbar.objects.filter(navbarorderableoverride__in=navbarorderables).order_by("navbarorderable__sort_order")

    #use original navbar unless new one is defined
    if navbars.count() == 0:
        return { "navbars" : get_navbars({"request" : request}) }

    return { "navbars" : [navbar.localized for navbar in navbars] }

def footers (request):
    layout = LayoutSettingsOverride.for_request(request)
    footerorderables = layout.site_footer.all()
    footers = TranslatableFooter.objects.filter(footerorderableoverride__in=footerorderables).order_by("footerorderable__sort_order")

    #use original footer unless new one is defined
    if footers.count() == 0:
        return { "footers" : get_footers({"request" : request}) }

    return { "footers" : [footer.localized for footer in footers]}
