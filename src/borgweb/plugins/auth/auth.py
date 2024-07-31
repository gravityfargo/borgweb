""" plugins/auth/auth.py """

from borgweb.plugins import WebPlugin
import os, functools
from flask import current_app as app
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash
from borgweb.db import get_db


class Auth(WebPlugin):
    blueprint = Blueprint(
        "auth",
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        url_prefix="/auth",
    )

    @staticmethod
    @blueprint.before_app_request
    def load_logged_in_user():
        user_id = session.get("user_id")

        if user_id is None:
            g.user = None
        else:
            g.user = (
                get_db()
                .execute("SELECT * FROM user WHERE id = ?", (user_id,))
                .fetchone()
            )

    @staticmethod
    @blueprint.route("/login", methods=("GET", "POST"))
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            error = None
            user = db.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone()

            if user is None:
                error = "Incorrect username."
            elif not check_password_hash(user["password"], password):
                error = "Incorrect password."

            if error is None:
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("dashboard.index"))

            flash(error)

        return render_template("auth/login.html")

    @staticmethod
    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for("auth.login"))

            return view(**kwargs)

        return wrapped_view

    @staticmethod
    @blueprint.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("dashboard.index"))
