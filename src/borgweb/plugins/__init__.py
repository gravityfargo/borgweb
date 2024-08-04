""" plugins/__init__.py """

import os, traceback
from importlib import util
from inspect import getmembers, isclass
from flask import Blueprint
from flask import current_app as app
from abc import ABC, abstractmethod


class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def register_blueprints(self, enabled_plugins):
        """Register blueprints

        Reqires app context.

        Args:
            enabled_plugins (list): List of enabled plugins
        """
        for plugin in self.plugins:
            if plugin.plugin_name in enabled_plugins:
                app.register_blueprint(plugin.blueprint)
            else:
                del plugin

    def load_python_module(self, path):
        """Load a python module

        Args:
            path (str): Path to the python module

        Returns:
            module: The loaded module
        """
        name = os.path.split(path)[-1]
        spec = util.spec_from_file_location(name, path)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_plugins(self, plugin_dir: str):
        """Find and load all plugins in the plugin directory

        Args:
            plugin_dir (str): Path to the plugin directory
        """
        for i in os.listdir(plugin_dir):
            # ignore if is not a directory or starts with __
            if not os.path.isdir(os.path.join(plugin_dir, i)) or i.startswith("__"):
                continue

            for j in os.listdir(os.path.join(plugin_dir, i)):
                # ignore if is not a python file or starts with __
                if not j.endswith(".py") or j.startswith("__"):
                    continue

                try:
                    module = self.load_python_module(os.path.join(plugin_dir, i, j))
                    # get all classes from the module
                    objs = getmembers(module, isclass)
                    for name, obj in objs:
                        if issubclass(obj, Plugin) and obj != Plugin:
                            # create an instance of the class
                            plugin_instance = obj(os.path.join(plugin_dir, i))
                            self.register_plugin(plugin_instance)
                except Exception:
                    traceback.print_exc()

    def update_nav(self, nav_path):
        """Update the navigation bar with links for the enabled plugins

        Args:
            nav_path (str): Path to the nav.html file
        """
        if os.path.exists(nav_path):
            os.remove(nav_path)
            with open(nav_path, "w") as f:
                f.write("")

        for plugin in self.plugins:
            if not plugin.backend_only:
                href = f"url_for('{plugin.plugin_name}.index')"
                with open(nav_path, "a") as f:
                    f.write('<li class="nav-item">\n')
                    f.write(
                        '\t<a class="nav-link link-light" href="{{ ' + href + ' }}">\n'
                    )
                    f.write(
                        '\t\t<i class="bi '
                        + plugin.bootstrap_icon
                        + '"></i><span class="ms-1 d-none d-sm-inline">'
                        + plugin.nav_display_name
                        + "</span>\n"
                    )
                    f.write("\t</a>\n")
                    f.write("</li>\n")


class Plugin(ABC):
    """Abstract class for plugins

    Force subclasses to implement the following properties:
    - plugin_name: the name of the plugin
    - backend_only: indicating if the plugin will be in the side bar
    - nav_display_name: for the navigation bar
    - bootstrap_icon: for the navigation bar
    """

    def __init__(self, plugin_dir):
        """Constructor

        Args:
            plugin_dir (str): Path to the plugin's directory
        """
        if self.plugin_name == "dashboard":
            url_prefix = "/"
        else:
            url_prefix = f"/{self.plugin_name}"

        self.blueprint = Blueprint(
            self.plugin_name,
            self.__module__,
            template_folder=os.path.join(plugin_dir, "templates"),
            static_folder=os.path.join(plugin_dir, "static"),
            url_prefix=url_prefix,
        )
        self.setup_routes()

    @property
    @abstractmethod
    def plugin_name(self):
        pass

    @property
    @abstractmethod
    def backend_only(self):
        pass

    @property
    def nav_display_name(self):
        pass

    @property
    def bootstrap_icon(self):
        pass

    @abstractmethod
    def setup_routes(self):
        """
        Setup Flask routes for the plugin. This method must be implemented
        in each subclass to add routes to the `self.blueprint`.
        """
        pass
