import os
import bottle
import json

from foris import fapi

from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.plugins import ForisPlugin
from foris.state import current_state
from foris.utils.translators import gettext_dummy as gettext


class StoragePluginConfigHandler(BaseConfigHandler):
    userfriendly_title = gettext("storage")

    def get_form(self):
        form = fapi.ForisForm("storage", [])
        form.add_section(name="set_srv", title=self.userfriendly_title)

        return form


class StoragePluginPage(ConfigPageMixin, StoragePluginConfigHandler):
    slug = "storage"
    menu_order = 60
    template = "storage/storage"
    template_type = "jinja2"
    userfriendly_title = gettext("Storage")

    def render(self, **kwargs):
        kwargs['settings'] = current_state.backend.perform("storage", "get_settings")
        kwargs['settings']['old_device_name'] = \
            kwargs['settings']["old_device"].replace("/dev/", "")

        available_modules = current_state.backend.perform("introspect", "list_modules")
        if "nextcloud" in available_modules["modules"]:
            nextcloud_data = current_state.backend.perform("nextcloud", "get_status")
            kwargs["settings"]["nextcloud_installed"] = nextcloud_data["nextcloud_installed"]
            kwargs["settings"]["nextcloud_configured"] = nextcloud_data["nextcloud_configured"]
            kwargs["settings"]["nextcloud_configuring"] = nextcloud_data["nextcloud_configuring"]

        drives = current_state.backend.perform("storage", "get_drives")["drives"]
        kwargs['drives'] = sorted(drives, key=lambda d: d['dev'])
        return super(StoragePluginPage, self).render(**kwargs)

    def call_ajax_action(self, action):
        if action == 'get_settings':
            if bottle.request.method != 'GET':
                raise bottle.HTTPError(404, "Wrong http method (only GET is allowed.")

            data = current_state.backend.perform("storage", "get_settings")
            return data

        raise ValueError("Unknown AJAX action.")

class StoragePlugin(ForisPlugin):
    PLUGIN_NAME = "storage"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))

    PLUGIN_STYLES = [
        "css/storage.css",
    ]
    PLUGIN_STATIC_SCRIPTS = [
    ]
    PLUGIN_DYNAMIC_SCRIPTS = [
    ]

    def __init__(self, app):
        super(StoragePlugin, self).__init__(app)
        add_config_page(StoragePluginPage)
