from flask import render_template, Blueprint

settings_bp = Blueprint(
    "settings", __name__, template_folder="templates", static_folder="static"
)


@settings_bp.route("/settings", methods=["GET"])
def settings():
    return render_template("settings.html")
