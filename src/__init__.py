import os

from foris import fapi, validators

from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.form import Textbox, Checkbox, Number
from foris.plugins import ForisPlugin
from foris.state import current_state
from foris.utils.translators import gettext_dummy as gettext, ugettext as _


class StoragePluginConfigHandler(BaseConfigHandler):
    userfriendly_title = gettext("storage")

    def get_form(self):
        form = fapi.ForisForm("storage", [])
        main = form.add_section(name="set_srv", title=_(self.userfriendly_title))
        def form_cb(data):
            msg = {"drive": self.data["new_disk"]}
            current_state.backend.perform("storage", "prepare_srv_drive", msg)
            return "none", None
        form.add_callback(form_cb)

        return form


class StoragePluginPage(ConfigPageMixin, StoragePluginConfigHandler):
    menu_order = 60
    template = "storage_plugin/storage_plugin.tpl"
    userfriendly_title = gettext("Storage")

    def render(self, **kwargs):
        kwargs['settings'] = current_state.backend.perform("storage", "get_settings", {})
        tmp = current_state.backend.perform("storage", "get_drives", {})
        if not tmp:
            tmp = { "drives": []}
        kwargs['drives'] = tmp['drives']
        return super(StoragePluginPage, self).render(**kwargs)

class StoragePlugin(ForisPlugin):
    PLUGIN_NAME = "storage_plugin"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))

    PLUGIN_STYLES = [
    ]
    PLUGIN_STATIC_SCRIPTS = [
    ]
    PLUGIN_DYNAMIC_SCRIPTS = [
    ]

    def __init__(self, app):
        super(StoragePlugin, self).__init__(app)
        add_config_page("storage_plugin", StoragePluginPage, top_level=True)
