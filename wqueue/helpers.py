import collections


def merge_dicts(first_dict, second_dict):
    for key, value in second_dict.items():
        if (key in first_dict and isinstance(first_dict[key], dict)
                and isinstance(second_dict[key], collections.Mapping)):
            merge_dicts(first_dict[key], second_dict[key])
        else:
            first_dict[key] = second_dict[key]
