""" plugins/auth/auth.py """

from borgweb.plugins import Plugin
from flask_login import login_user, logout_user, login_required
from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.security import check_password_hash
from borgweb.database.models import User


class Auth(Plugin):
    backend_only = True
    plugin_name = "auth"

    def setup_routes(self):
        @self.blueprint.route("/login")
        def login():
            return render_template("auth/login.html")

        @self.blueprint.route("/login", methods=["POST"])
        def login_post():
            username = request.form.get("username")
            password = request.form.get("password")
            remember = True if request.form.get("remember") else False

            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                flash("Please check your login details and try again.")
                return redirect(url_for("auth.login"))
            login_user(user, remember=remember)
            return redirect(url_for("dashboard.index"))

        @self.blueprint.route("/logout")
        @login_required
        def logout():
            logout_user()
            return redirect(url_for("dashboard.index"))
