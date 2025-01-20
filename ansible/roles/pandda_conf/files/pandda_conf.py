import ipaddress
import os
import sys
from argparse import ArgumentParser
from grp import getgrnam
from pathlib import Path
from pwd import getpwnam

import yaml


def validate_prefixes(prefixes: list):
    for prefix in prefixes:
        _ip = ipaddress.ip_network(prefix)
    return prefixes


def yml_prefixes(config: dict, fp):
    """Generate a YAML file with prefixes for ADiCT IP filter"""
    prefixes = validate_prefixes(config["protected_prefixes"])
    yaml.dump({"prefixes": prefixes}, fp)


def unirecfilter_uniflow_prefixes(config: dict, fp):
    """Generate a unirecfilter configuration file with prefixes for uniflow

    Format:

        # Selected prefixes - both directions
        :
        SRC_IP == 192.168.56.0/21 || DST_IP == 192.168.56.0/21;
        # Selected prefixes - outgoing traffic only
        :
        SRC_IP == 192.168.56.0/21;
    """
    prefixes = validate_prefixes(config["protected_prefixes"])

    bidir = " ||\n".join([f"SRC_IP == {p} || DST_IP == {p}" for p in prefixes])
    outgoing = " ||\n".join([f"SRC_IP == {p}" for p in prefixes])

    fp.write(f"# This file contains prefixes generated from this host's pandda.conf\n")
    fp.write(f"# Selected prefixes - both directions\n")
    fp.write(f":\n")
    fp.write(f"{bidir};\n")
    fp.write(f"# Selected prefixes - outgoing traffic only\n")
    fp.write(f":\n")
    fp.write(f"{outgoing};\n")


def unirecfilter_biflow_prefixes(config: dict, fp):
    """
    Generate a unirecfilter configuration file with prefixes for biflow

    Format:

        # Selected prefixes - incoming traffic only
        :
        DST_IP == 192.168.56.0/21;
    """
    prefixes = validate_prefixes(config["protected_prefixes"])

    incoming = " ||\n".join([f"DST_IP == {p}" for p in prefixes])

    fp.write(f"# This file contains prefixes generated from this host's pandda.conf\n")
    fp.write(f"# Selected prefixes - incoming traffic only\n")
    fp.write(f":\n")
    fp.write(f"{incoming};\n")


def nemea_adict_prefixes(config: dict, fp):
    """Generate a NEMEA ADiCT configuration file with prefixes

    Format:

        # This file contains prefixes generated from this host's pandda.conf
        192.168.56.0/21
    """
    prefixes = validate_prefixes(config["protected_prefixes"])

    fp.write(f"# This file contains prefixes generated from this host's pandda.conf\n")
    for prefix in prefixes:
        fp.write(f"{prefix}\n")


generators = {
    "ip_filter.yml": yml_prefixes,
    "prefix_filter_single": unirecfilter_uniflow_prefixes,
    "prefix_filter_bi": unirecfilter_biflow_prefixes,
    "prefixes.conf": nemea_adict_prefixes,
}


def generate_objects(config: dict, objects: list):
    """Go through the list of objects and generate the configuration files"""
    for o in objects:
        assert len(o) == 1, f"Object {o} must have exactly one key"
        name, conf = list(o.items())[0]

        assert (
            name in generators
        ), f"Unknown name {name}, use one of {generators.keys()}"

        for key in ["dest", "owner", "group", "mode"]:
            assert key in conf, f"Key {key} missing for object {name}"

        dest = conf["dest"]
        dest_path = Path(dest)
        if dest_path.is_dir():
            assert dest_path.exists(), f"Destination {dest} does not exist"
            dest_path = dest_path / name
        else:
            assert dest_path.parent.exists(), f"Destination {dest} does not exist"

        with open(dest_path, "w") as f:
            generators[name](config, f)

        try:
            os.chown(
                dest_path,
                getpwnam(conf["owner"]).pw_uid,
                getgrnam(conf["group"]).gr_gid,
            )
        except KeyError as e:
            raise ValueError(f"No such user or group: {e}")
        os.chmod(dest_path, int(conf["mode"], 8))


if __name__ == "__main__":
    parser = ArgumentParser(description="Pandda configuration generator")
    parser.add_argument(
        "objects",
        help="configuration file specifying objects to generate",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        default="/etc/pandda.d/pandda.yaml",
        help="configuration file containing user settings",
    )
    args = parser.parse_args()

    adict_config = None
    if os.path.exists(args.config):
        with open(args.config, "r") as f:
            pandda_config = yaml.safe_load(f)
        for sub_config in pandda_config:
            if "adict" in sub_config:
                adict_config = sub_config["adict"]
                break
        else:
            print("adict section missing in the configuration file", file=sys.stderr)
            exit(1)
    else:
        print(f"Configuration file {args.config} not found", file=sys.stderr)
        exit(1)

    if os.path.exists(args.objects):
        with open(args.objects, "r") as f:
            objects = yaml.safe_load(f)
    else:
        print(f"Objects file {args.objects} not found", file=sys.stderr)
        exit(1)

    try:
        generate_objects(adict_config, objects)
    except KeyError as e:
        print(f"Key missing in the configuration file: {e}", file=sys.stderr)
        exit(1)
    except AssertionError as e:
        print(e, file=sys.stderr)
        exit(1)
    except ValueError as e:
        print(f"Invalid value in the configuration file: {e}", file=sys.stderr)
        exit(1)
