from borgweb.plugins import Plugin
from borgweb.settings import Config
from flask import render_template


class Backup(Plugin, Config):
    backend_only = False
    plugin_name = "backup"
    bootstrap_icon = "bi-floppy2-fill"
    nav_display_name = "Backup"

    def setup_routes(self):
        repo_list = self.get_config_value("repo_list", "repos")

        @self.blueprint.route("/")
        def index():
            nonlocal repo_list
            print(repo_list)
            return render_template("backup/backup_info.html", repo_list=repo_list)

        @self.blueprint.route("/repo/<repo_name>")
        def repo_info(repo_name):
            nonlocal repo_list
            repo_config = self.get_config_value("repositories", "repos").get(repo_name, {})
            repo = repo_list.get(repo_name)

            return render_template("backup/repo_info.html", repo=repo)

        @self.blueprint.route("/repo/<repo_name>/<")
        def repo_info(repo_name):
            nonlocal repo_list
            repo_config = self.get_config_value("repositories", "repos").get(repo_name, {})
            repo = repo_list.get(repo_name)

            return render_template("backup/repo_info.html", repo=repo)