offshell
===============
`offshell` opens an interactive shell into your offscale node. It uses paramiko, a Python implementation of the SSHv2 protocol

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## Usage

    $ python -m offshell -h
    usage: __main__.py [-h] -n NAME [--version] [--etcd ETCD] [--purpose PURPOSE]
                       [--load-system-host-keys LOAD_SYSTEM_HOST_KEYS]
    
    offshell opens an interactive shell into your offscale node
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  Name of node. /{purpose}/{node_name} will overwrite
                            `--purpose`.
      --version             show program's version number and exit
      --etcd ETCD           Server location [127.0.0.1:4001]
      --purpose PURPOSE, --cluster PURPOSE
                            Purpose of the node. Groups all together
                            (hierarchically). Defaults to: 'unclustered'
      --load-system-host-keys LOAD_SYSTEM_HOST_KEYS
                            Load host keys from a system (read-only) file.

Sane defaults means usually you just:

    $ python -m offshell -n node_name
