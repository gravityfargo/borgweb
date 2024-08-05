from borgweb.plugins import Plugin
from borgweb.settings import Config
from flask import render_template

class Settings(Plugin, Config):
    backend_only = False
    plugin_name = "settings"
    bootstrap_icon = "bi-gear"
    nav_display_name = "Settings"

    default_config = {
        "defaults": {
            "archive_name": "archive-{hostname}-{now}"
            "create_backup_command": "borg create --list REPO_DIRECTORY::ARCHIVE_NAME ."
        }
    }

    def setup_routes(self):
        @self.blueprint.route("/")
        def index():
            return render_template("settings/index.html")
