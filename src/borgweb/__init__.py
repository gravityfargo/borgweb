""" __init__.py """

from ._version import version
import os
from flask import Flask
from . import db
from .plugins import WebPlugin


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    for plugin in WebPlugin.plugins:
        plugin()
        app.register_blueprint(plugin.blueprint)

    # app.config.from_object('config.Config')
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "borgweb.sqlite"),
    )

    db.init_app(app)

    @app.context_processor
    def utility_processor():
        return dict(version=version)

    return app
