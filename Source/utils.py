import yaml

CONFIG_PATH = "Source/config/config.yml"

def load_config(config_name):
    with open(config_name) as file:
        config = yaml.safe_load(file)

    return config
