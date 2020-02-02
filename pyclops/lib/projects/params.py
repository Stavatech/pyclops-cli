from pyclops.lib.io.modules import load_module


def load_params(name, path, stage=None):
    params_module = load_module(name, path)
    params = {k:v for k,v in params_module.__dict__.items() if not k.startswith("__")}

    if stage:
        params['stage'] = stage
        stage_params = params['stages'][stage]
        for key in stage_params.keys():
            params['stage_%s' % key] = stage_params[key]
    
    return params
