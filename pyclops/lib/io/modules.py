import importlib


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    return params