import sys
import os
import yaml

def main():
    # ./ipfixprobe_conf.py pandda.yaml output
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <pandda.yaml> <output_dir>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    output_dir = sys.argv[2]

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

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for probe in probes:
        instance_name = probe.get('instance_name', 'unknown')
        output_filename = f"instance_{instance_name}.conf"
        output_path = os.path.join(output_dir, output_filename)
        del probe['instance_name']
        with open(output_path, 'w') as out_f:
            yaml.dump(probe, out_f, default_flow_style=False)

if __name__ == "__main__":
    main()
