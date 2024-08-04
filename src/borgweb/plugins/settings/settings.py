""" plugins/settings/settings.py """

from borgweb.plugins import Plugin
from flask import render_template

class Settings(Plugin):
    backend_only = False
    plugin_name = "settings"
    bootstrap_icon = "bi-gear"
    nav_display_name = "Settings"

    def setup_routes(self):
        @self.blueprint.route("/")
        def index():
            return render_template("settings/index.html")
