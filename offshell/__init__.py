#!/usr/bin/env python

from __future__ import print_function

import logging
import sys
import traceback
from collections import namedtuple
from json import loads
from logging.config import dictConfig as _dictConfig
from os import path
from os.path import exists, expanduser
from sys import stderr

import etcd3
import paramiko
import yaml
from libcloud.compute.types import NodeState
from offutils_strategy_register import dict_to_node
from paramiko.ssh_gss import GSS_AUTH_AVAILABLE

__author__ = "Samuel Marks"
__version__ = "0.0.5"

from offutils.util import iteritems


def get_logger(name=None):
    with open(path.join(path.dirname(__file__), "_data", "logging.yml"), "rt") as f:
        data = yaml.safe_load(f)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()

logging.getLogger("paramiko").setLevel(logging.CRITICAL)


def offshell(name, load_system_host_keys, load_ssh_config, ssh_config, etcd):
    """
    Offshell

    :param name: Name of node. /{purpose}/{node_name} will overwrite `--purpose`.
    :type name: ```str```

    :param load_system_host_keys: Load host keys from a system (read-only) file.
    :type load_system_host_keys: ```str```

    :param load_ssh_config: Load SSH config from a system (read-only) file.
    :type load_ssh_config: ```Optional[str]```

    :param ssh_config: SSH config
    :type ssh_config: ```dict```

    :param etcd: "host:port" connection string to etcd
    :type etcd: ```str```
    """
    host, port = etcd.split(":")
    node = dict_to_node(loads(etcd3.client(host=host, port=int(port)).get(name)[0]))
    if node.state != NodeState.RUNNING:
        raise EnvironmentError(
            "Node isn't running, it's {}. Ensure it's ON, then try again.".format(
                node.state
            )
        )

    connection_d = {
        "hostname": node.public_ips[0],
        "username": node.extra["user"]
        if "user" in node.extra
        else node.extra.get("ssh_config", {}).get("User"),
        "password": node.extra.get("password"),
        "key_filename": node.extra.get("ssh_config", {}).get("IdentityFile"),
    }

    if ssh_config:
        if not connection_d["key_filename"]:
            root_logger.warning(
                "Cannot set password in ssh_config format. You'll still be prompted."
            )
        tab = " " * 4

        if "ssh_config" in node.extra and len(node.extra["ssh_config"]) > 1:
            host = node.extra["ssh_config"].pop("Host")
            print(
                "Host {host}\n{rest}".format(
                    host=host,
                    rest=tab
                    + tab.join(
                        "{} {}\n".format(k, v[0] if isinstance(v, list) else v)
                        for k, v in iteritems(node.extra["ssh_config"])
                    )[:-1],
                )
            )

        else:
            print(
                "Host {name}\n"
                "{tab}HostName {hostname}\n"
                "{tab}User {username}\n"
                "{last_line}".format(
                    name=name.rpartition("/")[2],
                    hostname=connection_d["hostname"],
                    username=connection_d["username"],
                    tab=tab,
                    last_line="{tab}IdentityFile {key_filename}".format(
                        tab=tab, key_filename=connection_d["key_filename"]
                    )
                    if connection_d["key_filename"]
                    else "",
                )
            )
        known_hosts = path.join(expanduser("~"), ".ssh", "known_hosts")
        s = ""
        if exists(known_hosts):
            with open(known_hosts, "rt") as f:
                s = f.read()
        if connection_d["hostname"] not in s:
            print(
                "After checking the key fingerprint, add it to your known hosts with:"
                "\nssh-keyscan {host} >> {known_hosts}".format(
                    host=connection_d["hostname"], known_hosts=known_hosts
                ),
                file=stderr,
            )
        return

    # Paramiko client configuration
    UseGSSAPI = GSS_AUTH_AVAILABLE  # enable "gssapi-with-mic" authentication, if supported by your python installation
    DoGSSAPIKeyExchange = GSS_AUTH_AVAILABLE  # enable "gssapi-kex" key exchange, if supported by your python installation
    # UseGSSAPI = False
    # DoGSSAPIKeyExchange = False
    port = 22

    hostname = connection_d["hostname"]
    if hostname.find(":") >= 0:
        hostname, portstr = hostname.split(":")
        port = int(portstr)
        print("hostname:", hostname, ";")

    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    client = namedtuple("_", ("close",))(lambda _: _)
    try:
        client = paramiko.SSHClient()
        if load_system_host_keys:
            client.load_system_host_keys()
        if path.isfile(load_ssh_config):
            # Same runaround that Fabric/Invoke does
            config = paramiko.SSHConfig()
            with open(load_ssh_config, "rt") as f:
                config.parse(f)
            config_options = config.lookup(connection_d["hostname"])
            connection_d["hostname"] = config_options["hostname"]

        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        if not UseGSSAPI and not DoGSSAPIKeyExchange:
            client.connect(**connection_d)

        chan = client.invoke_shell()
        interactive.interactive_shell(chan)
        chan.close()
        client.close()

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        client.close()
        sys.exit(1)
