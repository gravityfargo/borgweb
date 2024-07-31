from flask import render_template, Blueprint

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")
