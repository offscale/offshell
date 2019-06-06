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
      -o, --ssh-config      Output SSH config format. Don't connect.

Sane defaults means usually you just:

    $ python -m offshell -n node_name

If you prefer to use `ssh`, you can use this to add nodes to your ssh_config like so:
    
    $ python -m offshell -n node_name --ssh-config >> ~/.ssh/config

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
