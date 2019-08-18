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


def process_dir(path, params={}, build_dir=DEFAULT_BUILD_DIR):
    templates = glob.glob(os.path.join(path, "**/*.jinja"), recursive=True)
    
    for template in templates:
        template = template[len(path):]
        
        input_template_path = os.path.join(path, template)
        output_template_path = os.path.join(build_dir, template)[:-6]

        template_build_dir = os.path.dirname(output_template_path)
        os.makedirs(template_build_dir, exist_ok=True)

        rendered_template = process_template(path=input_template_path, params=params)

        with open(output_template_path, 'w') as rendered_template_file:
            print(rendered_template, file=rendered_template_file)
            print("Generated %s" % output_template_path)
        
