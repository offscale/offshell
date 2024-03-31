# -*- coding: utf-8 -*-
"""
offshell command-line interface
"""

from argparse import ArgumentParser
from os import path
from os.path import expanduser
from sys import modules

from offshell import __version__, offshell


def _build_parser():
    """
    CLI parser builder using builtin `argparse` module

    :return: instanceof ArgumentParser
    :rtype: ```ArgumentParser```
    """
    parser = ArgumentParser(
        description="offshell opens an interactive shell into your offscale node."
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name of node. /{purpose}/{node_name} will overwrite `--purpose`.",
        required=True,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="{} {}".format(modules[__name__].__package__, __version__),
    )
    parser.add_argument(
        "--etcd", help="Server location\t[127.0.0.1:2379]", default="127.0.0.1:2379"
    )
    parser.add_argument(
        "--purpose",
        "--cluster",
        dest="purpose",
        default="unclustered",
        help="Purpose of the node. Groups all together (hierarchically). Defaults to: 'unclustered'",
    )
    parser.add_argument(
        "--load-system-host-keys",
        dest="load_system_host_keys",
        default=True,
        help="Load host keys from a system (read-only) file.",
    )
    parser.add_argument(
        "--load-ssh-config",
        default=path.join(expanduser("~"), ".ssh", "config"),
        help="Load SSH config from a system (read-only) file.",
    )
    parser.add_argument(
        "-o",
        "--ssh-config",
        dest="ssh_config",
        action="store_true",
        help="Output SSH config format. Don't connect.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    if args.purpose and not args.name.startswith("/"):
        args.name = "/".join((args.purpose, args.name))
        args.purpose = None

    offshell(**dict((k, v) for k, v in args._get_kwargs() if v is not None))
