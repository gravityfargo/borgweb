from flask import render_template, Blueprint

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["GET"])
def logs():
    return render_template("logs.html")
