import os
import glob
import jinja2


DEFAULT_BUILD_DIR = os.path.join(
    os.getenv('BUILD_DIR', './build'),
    'jinja'
)


def process_template(path, params={}):
    rendered_template = None
    with open(path, 'r') as template_file:
        template = jinja2.Template(template_file.read())
        rendered_template = template.render(**params)
    return rendered_template


def process_dir(path, params={}, in_place=False, build_dir=DEFAULT_BUILD_DIR, suffix=".jinja", remove_suffix=False):
    templates = glob.glob(os.path.join(path, "**/*%s" % suffix), recursive=True)
    
    for template in templates:
        if os.path.isdir(template):
            continue
        
        template = template[len(path):]
        
        input_template_path = os.path.join(path, template)

        if in_place:
            output_template_path = input_template_path
        else:
            output_template_path = os.path.join(build_dir, template)[:-6]
            template_build_dir = os.path.dirname(output_template_path)
            os.makedirs(template_build_dir, exist_ok=True)
        
        if remove_suffix:
            if output_template_path.endswith(suffix):
                output_template_path = output_template_path[:-len(suffix)]

        rendered_template = process_template(path=input_template_path, params=params)

        with open(output_template_path, 'w') as rendered_template_file:
            print(rendered_template, file=rendered_template_file)
            print("Generated %s" % output_template_path)  
