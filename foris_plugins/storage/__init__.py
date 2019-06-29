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

        def form_cb(data):
            msg = {"drive": self.data["new_disk"]}
            current_state.backend.perform("storage", "prepare_srv_drive", msg)
            return "none", None
        form.add_callback(form_cb)

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
        drives = current_state.backend.perform("storage", "get_drives")["drives"]
        kwargs['drives'] = sorted(drives, key=lambda d: d['dev'])
        return super(StoragePluginPage, self).render(**kwargs)

    def call_ajax_action(self, action):
        if action == "configure_nextcloud":
            if bottle.request.method != 'POST':
                raise bottle.HTTPError(404, "Wrong http method (only POST is allowed.")

            data = bottle.request.POST.get('credentials', {})
            data = current_state.backend.perform("storage", "configure_nextcloud", credentials)
            return data
        elif action == 'get_settings':
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
