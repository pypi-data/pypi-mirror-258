# -*- coding: utf-8 -*-
from collective.plausible import _
from collective.plausible.interfaces import ICollectivePlausibleLayer
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IPlausibleControlPanel(Interface):
    url = schema.TextLine(
        title=_("Plausible URL"),
        description=_("Example : plausible.imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    site = schema.TextLine(
        title=_("Plausible Site"),
        description=_("Example : imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    token = schema.TextLine(
        title=_("Plausible token"),
        description=_("Plausible authentification token"),
        default="",
        required=False,
        readonly=False,
    )

    link_user_action = schema.Bool(
        title=_("Add a link in the user menu"),
        description=_("Add a link to the statistics browser view in the user menu"),
        default=True,
        required=False,
        readonly=False,
    )


class PlausibleControlPanel(RegistryEditForm):
    schema = IPlausibleControlPanel
    schema_prefix = "collective.plausible"
    label = _("Plausible Control Panel")


class ControlPanelFormView(layout.FormWrapper):
    index = ViewPageTemplateFile("controlpanel.pt")


PlausibleControlPanelView = layout.wrap_form(
    PlausibleControlPanel, ControlPanelFormView
)


@adapter(Interface, ICollectivePlausibleLayer)
class PlausibleControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IPlausibleControlPanel
    configlet_id = "plausible_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("Plausible Control Panel")
    group = ""
    schema_prefix = "collective.plausible.plausible_control_panel"
