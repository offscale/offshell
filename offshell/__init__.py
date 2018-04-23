#!/usr/bin/env python

from json import loads

import yaml
import logging

from os import path
from logging.config import dictConfig as _dictConfig

from etcd import Client
from libcloud.compute.types import NodeState
from offutils_strategy_register import dict_to_node
from paramiko import SSHClient

from offshell.interactive import interactive_shell

__author__ = 'Samuel Marks'
__version__ = '0.0.1'


def get_logger(name=None):
    with open(path.join(path.dirname(__file__), '_data', 'logging.yml'), 'rt') as f:
        data = yaml.load(f)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()

logging.getLogger('paramiko').setLevel(logging.CRITICAL)


def open_shell(name, load_system_host_keys, etcd):
    host, port = etcd.split(':')
    node = dict_to_node(loads(Client(host=host, port=int(port)).get(name).value))
    if node.state != NodeState.RUNNING:
        raise EnvironmentError('Node isn\'t running, it\'s {}. Ensure it\'s ON, then try again.'.format(node.state))

    client = SSHClient()
    if load_system_host_keys:
        client.load_system_host_keys()
    client.connect(node.public_ips[0],
                   username=node.extra['user'] if 'user' in node.extra
                   else node.extra.get('ssh_config', {}).get('User'),
                   password=node.extra.get('password'),
                   key_filename=node.extra.get('ssh_config', {}).get('IdentityFile')
                   )
    chan = client.invoke_shell()
    interactive_shell(chan)
    chan.close()
    client.close()
