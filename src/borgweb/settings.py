from dotenv import dotenv_values
from abc import ABC, abstractmethod
import os, yaml, click
from borg.repository import Repository

# python -c 'import secrets; print(secrets.token_hex())'
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_secret_config() -> dict[str, str]:
    """Get the configuration from the .env file

    Returns:
        dict[str, str]: KEY=VALUE pairs from the .env file
    """

    config = ".env"
    default_config = {
        "BACKUP_CMD": "BORG_LOGGING_CONF=logging.conf borg create --list --stats --show-version --show-rc {REPOSITORY}::{NAME}-{LOCALTIME} /etc >{LOG_DIR}/{NAME}-{LOCALTIME} 2>&1 </dev/null",
        "SECRET_KEY": "dev",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///borgweb.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": "False",
        "ENABLED_PLUGINS": ["auth", "dashboard", "backup", "repos", "settings"],
    }

    loaded_config = dotenv_values(config)
    if len(loaded_config) == 0:
        with open(config, "w") as f:
            for key, value in default_config.items():
                if type(value) == list:
                    value = ",".join(value)
                f.write(f"{key}={value}\n")
        quit(
            "Configuration file created. Please edit it before running the application again."
        )

    for key, value in default_config.items():
        if key.startswith("FLASK_"):
            os.environ[key] = os.getenv(key, value)

    loaded_config["NAV_PATH"] = os.path.join(current_dir, "templates", "nav.html")
    loaded_config["PLUGINS_DIR"] = os.path.join(current_dir, "plugins")
    loaded_config["ENABLED_PLUGINS"] = loaded_config["ENABLED_PLUGINS"].split(",")
    return loaded_config


class Config(ABC):
    config_file = os.path.join(current_dir, "config.yaml")

    def get_config(self) -> dict:
        empty_config = {}
        if not os.path.exists(self.config_file):
            with open(self.config_file, "w") as f:
                yaml.dump({}, f)
            return empty_config
        else:
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f)

            if not config.get(self.plugin_name.upper()):
                config[self.plugin_name.upper()] = None
                with open(self.config_file, "w") as f:
                    yaml.dump(config, f)
                return empty_config
            return config[self.plugin_name.upper()]

    def get_config_value(self, key: str, plugin_name: str = None):
        """Get a value from the configuration

        Args:
            key (str): The key to get the value of
            plugin_name (str, optional): The name of the plugin to get the configuration from. Defaults to None.
        """
        real_plugin_name = self.plugin_name

        if plugin_name is not None:
            self.plugin_name = plugin_name
            config = self.get_config()
            self.plugin_name = real_plugin_name
        else:
            config = self.get_config()
        print(config)
        return config.get(key, "")

    def save_config(self, config: dict):
        """Save the configuration to the config file

        Will be saved in the format:
            `UPPER_PLUGIN_NAME: config`
        Args:
            config (dict): The configuration to save
        """
        plugin_config = {self.plugin_name.upper(): config}
        with open(self.config_file, "w") as f:
            yaml.dump(plugin_config, f)

    def config_update(self, key: str, value: str):
        """Update a key in the configuration

        You do not need to update the entire configuration,
        just the key you want to change.

        The configuration file will be created if it does not exist.

        Args:
            key (str): name of the key to update
            value (str): value to update the key with
        """
        config = self.get_config()
        config[key] = value
        self.save_config(config)


# [repository]
# version = 1
# segments_per_dir = 1000
# max_segment_size = 524288000
# append_only = 0
# storage_quota = 0
# additional_free_space = 0
# id = e8b1e86e20022de86e8eb6040e6e85aa3678d11f4bc914d1436a0d985f5aaafc


def read_repo_config(path: str) -> dict:
    conf = {}
    with open(os.path.join(path, "config"), "r") as f:
        for line in f:
            if line.startswith("[repository]"):
                continue
            line = line.strip().split(" = ")
            if len(line) > 1:
                conf[line[0]] = line[1]
    return conf


@click.command("test")
def test():
    path = "/tmp/test"
    repo = Repository(path)
    print(repo.is_repository(path))
