""" plugins/logs/logs.py """

from borgweb.plugins import Plugin
from flask import render_template


class Logs(Plugin):
    backend_only = False
    plugin_name = "logs"
    bootstrap_icon = "bi-journal"  # bi-file-text
    nav_display_name = "Logs"
    

    def setup_routes(self):
        @self.blueprint.route("/")
        def index():
            return render_template("logs/index.html")
