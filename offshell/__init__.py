#!/usr/bin/env python

from __future__ import print_function

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
__version__ = '0.0.2'


def get_logger(name=None):
    with open(path.join(path.dirname(__file__), '_data', 'logging.yml'), 'rt') as f:
        data = yaml.load(f)
    _dictConfig(data)
    return logging.getLogger(name=name)


root_logger = get_logger()

logging.getLogger('paramiko').setLevel(logging.CRITICAL)


def offshell(name, load_system_host_keys, ssh_config, etcd):
    host, port = etcd.split(':')
    node = dict_to_node(loads(Client(host=host, port=int(port)).get(name).value))
    if node.state != NodeState.RUNNING:
        raise EnvironmentError('Node isn\'t running, it\'s {}. Ensure it\'s ON, then try again.'.format(node.state))

    connection_d = {'hostname': node.public_ips[0],
                    'username': node.extra['user'] if 'user' in node.extra
                    else node.extra.get('ssh_config', {}).get('User'),
                    'password': node.extra.get('password'),
                    'key_filename': node.extra.get('ssh_config', {}).get('IdentityFile')}
    if ssh_config:
        if not connection_d['key_filename']:
            root_logger.warn('Cannot set password in ssh_config format. You\'ll still be prompted.')
        tab = ' ' * 4

        if 'ssh_config' in node.extra and len(node.extra['ssh_config'].keys()) > 1:
            host = node.extra['ssh_config'].pop('Host')
            print('Host {host}\n{rest}'
                  .format(host=host,
                          rest=tab + tab.join('{} {}\n'.format(k, v)
                                              for k, v in node.extra['ssh_config'].iteritems())[:-1]))
        else:
            print('Host {hostname}\n'
                  '{tab}User {username}{last_line}'
                  .format(hostname=connection_d['hostname'], tab=tab,
                          username=connection_d['username'],
                          last_line='\n{tab}IdentityFile {key_filename}'.format(tab=tab,
                                                                                key_filename=connection_d[
                                                                                    'key_filename'])
                          if connection_d['key_filename'] else ''))
        return

    client = SSHClient()
    if load_system_host_keys:
        client.load_system_host_keys()
    client.connect(**connection_d)
    chan = client.invoke_shell()
    interactive_shell(chan)
    chan.close()
    client.close()
