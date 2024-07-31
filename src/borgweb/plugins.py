import os
import json
from flask import Flask, Blueprint


def add_nav_item(app, plugin_info):
    if "nav_items" not in app.config:
        app.config["nav_items"] = []
    app.config["nav_items"].append(
        {"name": plugin_info["name"], "url": f"/{plugin_info['name']}/"}
    )


def load_plugins(app):
    plugins_dir = os.path.join(app.root_path, "plugins")
    for plugin_name in os.listdir(plugins_dir):
        plugin_dir = os.path.join(plugins_dir, plugin_name)
        if os.path.isdir(plugin_dir):
            info_path = os.path.join(plugin_dir, "info.json")
            config_path = os.path.join(plugin_dir, "config.json")  # Configuration file
            if os.path.exists(info_path):
                with open(info_path) as f:
                    info = json.load(f)
                if info.get("enabled", False):  # Checking if the plugin is enabled
                    if os.path.exists(config_path):  # Load plugin config if exists
                        with open(config_path) as f:
                            config = json.load(f)
                        app.config.update(
                            config
                        )  # Update app config with plugin config
                    # Import the plugin module
                    module = __import__(
                        f"plugins.{plugin_name}", fromlist=["init_plugin"]
                    )
                    bp = module.init_plugin()
                    app.register_blueprint(bp)
                    # Optionally, add navigation item dynamically
                    add_nav_item(app, info)
