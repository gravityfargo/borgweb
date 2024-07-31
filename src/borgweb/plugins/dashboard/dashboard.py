""" plugins/dashboard/dashboard.py """

from borgweb.plugins import WebPlugin
from flask import Blueprint, render_template
from flask import current_app as app
import os


class Dashboard(WebPlugin):
    blueprint = Blueprint(
        "dashboard",
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    @staticmethod
    @blueprint.route("/")
    def index():
        return render_template("dashboard/index.html")
