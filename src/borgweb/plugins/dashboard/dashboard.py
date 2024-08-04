from borgweb.plugins import Plugin
from flask import render_template

class Dashboard(Plugin):
    backend_only = False
    plugin_name = "dashboard"
    bootstrap_icon = "bi-speedometer2"
    nav_display_name = "Dashboard"

    def setup_routes(self):
        @self.blueprint.route("/")
        def index():
            return render_template("dashboard/index.html")
