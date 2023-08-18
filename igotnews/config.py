"""
 igotnews Config
"""
import os

from dynaconf import Dynaconf

# Define the root path of the project
ROOT = os.path.dirname(__file__)

# Load the default settings file
settings = Dynaconf(
    envvar_prefix="TT",
    # Set the root path of the project
    root_path=os.path.dirname(ROOT),
    # Load the default settings file
    settings_files=[
        os.path.join(ROOT, "default_settings.toml"),
        "talky_settings.toml",
        "settings.toml",
        ".secrets.toml",
    ],
    # Load the.env file
    load_dotenv=True,
    # merge=True,
    merge_enabled=True,
    # Set the environments to True
    environments=True,
    # Set the default environment
    default_env="default",
)
