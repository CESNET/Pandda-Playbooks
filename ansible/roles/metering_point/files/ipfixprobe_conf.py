#!/usr/bin/env python3
import sys
import os
import yaml
from jinja2 import Environment, FileSystemLoader

def main():
    # ./ipfixprobe_conf.py pandda.yaml instance_ipfixprobe.conf.j2 output
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <pandda.yaml> <template_file> <output_dir>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    template_file = sys.argv[2]
    output_dir = sys.argv[3]

    with open(yaml_file, 'r') as f:
        pandda_data = yaml.safe_load(f)
    probes = None
    if isinstance(pandda_data, list):
        for item in pandda_data:
            if 'probes' in item:
                probes = item['probes']
                break
    elif isinstance(pandda_data, dict) and 'probes' in pandda_data:
        probes = pandda_data['probes']

    if not probes:
        print("No 'probes' key found in the provided YAML.")
        sys.exit(2)

    template_dir = os.path.dirname(template_file)
    template_name = os.path.basename(template_file)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=False
    )
    template = env.get_template(template_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for probe in probes:
        rendered = template.render(item=probe)

        instance_name = probe.get('instance_name', 'unknown')
        output_filename = f"instance_{instance_name}.conf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w') as out_f:
            out_f.write(rendered)

if __name__ == "__main__":
    main()
