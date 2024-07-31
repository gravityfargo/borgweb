""" plugins/logs/logs.py """

from borgweb.plugins import WebPlugin
from flask import Blueprint, render_template
from flask import current_app as app
import os


class Logs(WebPlugin):
    blueprint = Blueprint(
        "logs",
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        url_prefix="/logs",
    )

    @staticmethod
    @blueprint.route("/")
    def index():
        return render_template("logs/index.html")
