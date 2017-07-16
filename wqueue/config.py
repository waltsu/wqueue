import copy

from wqueue.helpers import merge_dicts
from wqueue.defaults import DEFAULTS

_CONFIG = None


class ConfigurationException(Exception):
    pass


def get_config():
    if _CONFIG is None:
        raise ConfigurationException("No configuration set")
    return copy.deepcopy(_CONFIG)


def set_config(config=None):
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = merge_with_default_config(config)


def merge_with_default_config(config=None):
    new_config = copy.deepcopy(DEFAULTS)
    if config is not None:
        merge_dicts(new_config, config)

    return new_config
