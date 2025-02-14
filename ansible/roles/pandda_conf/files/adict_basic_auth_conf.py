import sys
import typing

import bcrypt
import yaml
from argparse import ArgumentParser


def generate_htpasswd_content(config: dict, output_file: typing.TextIO):
    """Generates htpasswd file content based on supplied central configuration file

    Args:
        config (dict): User configuration
        output_file (TextIO): Output file handle
    """
    for user in config:
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
        help="configuration string containing user settings",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-f",
        "--file",
        default="/etc/pandda.d/adict.htpasswd",
        help="output htpasswd file path"
    )
    args = parser.parse_args()

    # Load configuration
    users_config = yaml.safe_load(args.config)

    # Generate htpasswd
    with open(args.file, "w") as f:
        try:
            htpasswd_content = generate_htpasswd_content(users_config, f)
        except KeyError as e:
            print(f"Key missing in the configuration file: {e}", file=sys.stderr)
            exit(1)
