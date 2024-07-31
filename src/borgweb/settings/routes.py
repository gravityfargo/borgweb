from flask import render_template, Blueprint

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET"])
def settings():
    return render_template("settings.html")
