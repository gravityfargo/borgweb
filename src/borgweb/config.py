import os, click
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


@click.command("init-config")
def create_env():
    config = {
        "HOST": "127.0.0.1",
        "PORT": "5000",
        "DEBUG": "False",
        "REPOSITORY": "repo",
        "NAME": "localhost",
        "BACKUP_CMD": "BORG_LOGGING_CONF=logging.conf borg create --list --stats --show-version --show-rc {REPOSITORY}::{NAME}-{LOCALTIME} /etc >{LOG_DIR}/{NAME}-{LOCALTIME} 2>&1 </dev/null",
        "SECRET_KEY": "dev",
    }

    with open(".env", "w") as f:
        f.write("FLASK_APP=src/borgweb\n")
        f.write("FLASK_ENV=development\n")
        f.write("SECRET_KEY=dev\n")
        f.write("DATABASE=instance/borgweb.sqlite\n")


class Config(object):
    """This is the basic configuration class for BorgWeb."""
    pass
