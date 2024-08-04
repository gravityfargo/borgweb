from borgweb.plugins import Plugin
from flask import render_template, request, redirect, url_for
from flask import current_app as app


class Repos(Plugin):
    backend_only = False
    plugin_name = "repos"
    bootstrap_icon = "bi-box-seam"
    nav_display_name = "Repositories"

    def setup_routes(self):
        @self.blueprint.route("/")
        @self.blueprint.route("/<tab>")
        def index(tab="list-tab-pane"):
            return render_template("repos/index.html", tab=tab)

        @self.blueprint.route("/create", methods=["POST"])
        def new_repo():
            app.config.get("REPOS", [])
            repo = {
                request.form["name"]: {
                    "location": request.form["location"],
                    "description": request.form["description"],
                }
            }
            return redirect(url_for("repos.index"))
