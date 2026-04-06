import yaml
import os


def load_config():
    env = os.getenv("ENV", "qa")

    with open("config/env.yaml") as f:
        data = yaml.safe_load(f)

    return data[env]
