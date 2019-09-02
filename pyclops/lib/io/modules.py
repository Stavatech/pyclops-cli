import importlib


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_params(name, path):
    params_module = load_module(name, path)
    return {k:v for k,v in params_module.__dict__.items() if not k.startswith("__")}
