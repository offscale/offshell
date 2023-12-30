offshell
========
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech)
![Python version range](https://img.shields.io/badge/python-2.7%20|%203.5%20|%203.6%20|%203.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)
[![License](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT%20OR%20CC0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort)

`offshell` opens an interactive shell into your offscale node. It uses paramiko, a Python implementation of the SSHv2 protocol

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## Usage

    $ python -m offshell -h
    usage: __main__.py [-h] -n NAME [--version] [--etcd ETCD] [--purpose PURPOSE]
                       [--load-system-host-keys LOAD_SYSTEM_HOST_KEYS] [-o]
    
    offshell opens an interactive shell into your offscale node.
    
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
      --load-ssh-config LOAD_SSH_CONFIG
                            Load SSH config from a system (read-only) file
      -o, --ssh-config      Output SSH config format. Don't connect.

Sane defaults means usually you just:

    $ python -m offshell -n node_name

If you prefer to use `ssh`, you can use this to add nodes to your ssh_config like so:
    
    $ python -m offshell -n node_name --ssh-config >> ~/.ssh/config

## License

Licensed under any of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)
- CC0 license ([LICENSE-CC0](LICENSE-CC0) or <https://creativecommons.org/publicdomain/zero/1.0/legalcode>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
licensed as above, without any additional terms or conditions.
