from ._version import version
import os
from flask import Flask
from . import db


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "borgweb.sqlite"),
    )

    db.init_app(app)

    @app.context_processor
    def utility_processor():
        return dict(version=version)

    with app.app_context():
        from .dashboard import routes as dashboard
        from .auth import routes as auth
        from .logs import routes as logs
        from .api import routes as api
        from .settings import routes as settings
        from .repositories import routes as repositories

        app.register_blueprint(dashboard.dashboard_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(logs.logs_bp)
        app.register_blueprint(api.api_bp)
        app.register_blueprint(settings.settings_bp)
        app.register_blueprint(repositories.repos_bp)

        return app
