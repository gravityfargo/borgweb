from dotenv import dotenv_values
import os, yaml

# python -c 'import secrets; print(secrets.token_hex())'


def get_secret_config() -> dict[str, str]:
    """Get the configuration from the .env file

    Returns:
        dict[str, str]: KEY=VALUE pairs from the .env file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = ".env"

    default_config = {
        "BACKUP_CMD": "BORG_LOGGING_CONF=logging.conf borg create --list --stats --show-version --show-rc {REPOSITORY}::{NAME}-{LOCALTIME} /etc >{LOG_DIR}/{NAME}-{LOCALTIME} 2>&1 </dev/null",
        "SECRET_KEY": "dev",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///borgweb.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": "False",
        "ENABLED_PLUGINS": ["auth", "dashboard", "logs", "repos", "settings"],
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
