from ruamel.yaml import YAML


yaml = YAML()
yaml.preserve_quotes = True


def merge(yaml_files):
    """ Merge a list of YAML files into a single Python dictionary """
    print("Merging YAML files...")

    merged_dict = {}

    yaml_dicts = [read_yaml_file(x) for x in yaml_files]

    for yaml_dict in yaml_dicts:
        if yaml_dict is not None:
            _merge(yaml_dict, merged_dict)
    
    return merged_dict


def read_yaml_file(yaml_file):
    """ Read a YAML file into a Python dictionary """
    with open(yaml_file, 'r') as yaml_stream:
        yaml_dict = yaml.load(yaml_stream)
    return yaml_dict


def write_yaml_file(yaml_dict, file_name):
    """ Write a Python dictionary to file in YAML format """
    with open(file_name, 'w') as yaml_file:
        yaml.dump(yaml_dict, yaml_file)
    return file_name


def _merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            _merge(value, node)
        else:
            destination[key] = value

    return destination
