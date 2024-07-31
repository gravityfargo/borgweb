from flask import render_template, Blueprint

repos_bp = Blueprint("repos", __name__)


@repos_bp.route("/repos", methods=["GET"])
def repositories():
    return render_template("repositories.html")
