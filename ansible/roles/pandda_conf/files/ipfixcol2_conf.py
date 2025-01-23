import yaml
import os
from argparse import ArgumentParser
import xml
from string import Template 

output_template=Template("""
    <output>
        <name>$host forwarder</name>
        <plugin>forwarder</plugin>
        <params>
            <mode>all</mode>
            <protocol>$proto</protocol>
            <premadeConnections>0</premadeConnections>
            <hosts>
                <host>
                    <name>$host forwarder</name>
                    <address>$host</address>
                    <port>$port</port>
                </host>
            </hosts>
        </params>
    </output>
""")

input_template=Template("""
    <input>
        <name>$proto collector</name>
        <plugin>$proto</plugin>
        <params>
            <!-- List on port 4739 -->
            <localPort>$port</localPort>
            <!-- Bind to all local adresses -->
            <localIPAddress></localIPAddress>
        </params>
    </input>
""")


main_template=Template("""
<ipfixcol2>
    <!-- Input plugins -->
    <inputPlugins>
    $input_templates
    </inputPlugins>

    <outputPlugins>
    $output_templates

    <output>
        <name>Dummy output</name>
        <plugin>dummy</plugin>
        <params>
            <delay>0</delay>
            <stats>true</stats>
        </params>
    </output>
    </outputPlugins>
</ipfixcol2>
""")


def generate_ipfixcol2_conf(config: dict) -> str:
    #print(config)  
    inputs_spec = input_template.substitute(port=config["port"], proto=config["proto"].lower())
    
    output_spec = ""

    if "forward_targets" in config: 
        for target in config["forward_targets"]:
            output_spec += output_template.substitute(host=target["host"].lower(),
            port=target["port"], proto=target["proto"].lower())
    
    return main_template.substitute(input_templates=inputs_spec, output_templates=output_spec)

if __name__ == "__main__":
    parser = ArgumentParser(description="Pandda configuration generator")
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        default="/etc/pandda.d/pandda.yaml",
        help="configuration file containing user settings",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="/etc/ipfixcol2/ipfixcol2-startup.xml",
        help="output configuration file path"
    )
    args = parser.parse_args()

    collector_config = None
    if os.path.exists(args.config):
        with open(args.config, "r") as f:
            pandda_config = yaml.safe_load(f)
        for sub_config in pandda_config:
            if "collector" in sub_config:
                config = sub_config["collector"]
                break
        else:
            print("collector section missing in the configuration file", file=sys.stderr)
            exit(1)
    else:
        print(f"Configuration file {args.config} not found", file=sys.stderr)
        exit(1)
    try:
        conf_xml = generate_ipfixcol2_conf(config)
    except KeyError as e:
        print(f"Key missing in the configuration file: {e}", file=sys.stderr)
        exit(1)
    
    with open(args.file, "w") as f:
        f.write(conf_xml)