from borgweb._version import version
from flask import Flask
from flask_migrate import Migrate
from borgweb.plugins import PluginManager
from borgweb.database import db, Database
from borgweb.database.models import User
from borgweb.settings import get_secret_config, test
from flask_login import LoginManager


def register_commands(app):
    app.cli.add_command(Database.create_user)
    app.cli.add_command(test)

def create_app():
    config = get_secret_config()
    app = Flask(__name__)
    app.config.from_mapping(config)

    register_commands(app)
    plugin_manager = PluginManager()
    plugin_manager.load_plugins(config["PLUGINS_DIR"])

    db.init_app(app)
    migrate = Migrate(app, db)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def utility_processor():
        return dict(version=version)

    with app.app_context():
        # must setup plugins before setting up the database because plugins may
        # have models
        plugin_manager.register_blueprints(config["ENABLED_PLUGINS"])
        plugin_manager.update_nav(config["NAV_PATH"])
        db.create_all()
        return app


def main():
    app = create_app()
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])


if __name__ == "__main__":
    main()
