import copy

from wqueue.helpers import merge_dicts
from wqueue.defaults import DEFAULTS


def merge_with_default_config(config=None):
    new_config = copy.deepcopy(DEFAULTS)
    if config is not None:
        merge_dicts(new_config, config)

    return new_config
