import sys
import os
import typing

import bcrypt
import yaml
from argparse import ArgumentParser


def generate_htpasswd_content(config: dict, output_file: typing.TextIO):
    """Generates htpasswd file content based on supplied central configuration file

    Args:
        config (dict): Central configuration file
        output_file (TextIO): Output file handle
    """
    for user in config["users"]:
        # Data from config
        username = user["username"]
        password = user["password"]

        # Hash password using htpasswd's bcrypt mechanism
        hash_salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), hash_salt).decode("utf-8")

        f.write(f"{username}:{hashed_password}\n")


if __name__ == "__main__":
    parser = ArgumentParser(description="Pandda's ADiCT basic HTTP auth configuration generator")
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
        default="/etc/pandda.d/adict.htpasswd",
        help="output htpasswd file path"
    )
    args = parser.parse_args()

    # Load central config
    adict_config = None
    if os.path.exists(args.config):
        with open(args.config, "r") as f:
            pandda_config = yaml.safe_load(f)
        for sub_config in pandda_config:
            if "adict" in sub_config:
                adict_config = sub_config["adict"]
                break
        else:
            print("ADiCT section missing in the configuration file", file=sys.stderr)
            exit(1)
    else:
        print(f"Configuration file {args.config} not found", file=sys.stderr)
        exit(1)

    # Generate htpasswd
    with open(args.file, "w") as f:
        try:
            htpasswd_content = generate_htpasswd_content(adict_config, f)
        except KeyError as e:
            print(f"Key missing in the configuration file: {e}", file=sys.stderr)
            exit(1)
