from nautobot.extras.plugins import PluginTemplateExtension
from django.conf import settings
from packaging import version


class LocationTopologyButtons(PluginTemplateExtension):
    """
    Extend the DCIM location template to include content from this plugin.
    """
    model = 'dcim.location'

    def buttons(self):
        return self.render('nautobot_ui_plugin/location_topo_button.html')


# PluginTemplateExtension subclasses must be packaged into an iterable named
# template_extensions to be imported by NetBox.
template_extensions = [LocationTopologyButtons]
