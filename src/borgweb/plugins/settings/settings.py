""" plugins/settings/settings.py """

from borgweb.plugins import WebPlugin
from flask import Blueprint, render_template
from flask import current_app as app
import os


class Settings(WebPlugin):
    blueprint = Blueprint(
        "settings",
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        url_prefix="/settings",
    )

    @staticmethod
    @blueprint.route("/")
    def index():
        return render_template("settings/index.html")
