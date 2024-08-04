import os
from borgweb.plugins import Plugin
from borgweb.plugins.bash import Bash
from borgweb.settings import Config, read_repo_config
from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from borg.repository import Repository


class Repos(Plugin, Config):
    backend_only = False
    plugin_name = "repos"
    bootstrap_icon = "bi-box-seam"
    nav_display_name = "Repositories"

    def setup_routes(self):
        @self.blueprint.route("/")
        def index():
            self.config_update("a", "e")
            repos = self.get_config_value("repositories")
            if not repos:
                repos = {}
            return render_template("repos/repo_list.html", repos=repos)

        @self.blueprint.route("/import", methods=["POST"])
        def import_repo():
            existing = self.get_config_value("repositeories")
            if not existing or not isinstance(existing, dict):
                existing = {}
            new_repo = {
                request.form["name"]: {
                    "location": request.form["location"],
                    "description": request.form.get("description", ""),
                }
            }

            repo = Repository(request.form["location"])
            if request.path.endswith("import"):
                # print(repo.is_repository())
                print("import")

            existing.update(new_repo)
            self.config_update("repositories", existing)
            return redirect(url_for("repos.index"), code=200)

        @self.blueprint.route("/create", methods=["POST"])
        def create_repo():
            config = self.get_config_value("repositories")
            repo_list = self.get_config_value("repo_list")

            repo_name = request.form["name"]
            encryption = request.form.get("encryption", "none")
            location = request.form.get("location", "")
            new_repo = {
                repo_name: {
                    "location": location,
                    "encryption": encryption,
                    "description": request.form.get("description", ""),
                }
            }

            b = Bash(True, True)
            cmd = [
                "borg",
                "init",
                f"--encryption={encryption}",
                location,
            ]
            result = b.run(cmd)
            if result["returncode"] != 0:
                flash(cmd, "danger")
                flash(result["stderr"], "danger")
                return render_template("repos/create_repo.html")
            
            update_repo_list(repo_name)
            config.update(new_repo)
            
            self.config_update("repositories", config)
            
            return render_template(url_for("repos.index"))

        @self.blueprint.route("/form/<form_type>")
        def repo_form(form_type):
            if form_type == "import":
                return render_template("repos/import_repo.html")
            
            return render_template("repos/create_repo.html")

        @self.blueprint.route("/repo/<repo_name>")
        def repo_settings(repo_name):
            config = self.get_config_value("repositories")[repo_name]
            config.update(read_repo_config(config["location"]))
            
            return render_template("repos/repo_settings.html", config=config, repo_name=repo_name)

        def update_repo_list(repo_name):
            config = self.get_config_value("repo_list")
            if not isinstance(config, list):
                config = []
            config.append(repo_name)
            self.config_update("repo_list", config)