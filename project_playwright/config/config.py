import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "env.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)


def get_env(env_name="qa"):
    return CONFIG.get(env_name)
