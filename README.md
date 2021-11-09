<h1 align="center">Netbox DNS</h1>

<p align="center"><i>Netbox Dns is a netbox plugin for managing zone, nameserver and record inventory.</i></p>

<div align="center">
<a href="https://pypi.org/project/netbox-dns/"><img src="https://img.shields.io/pypi/v/netbox-dns" alt="PyPi"/></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/stargazers"><img src="https://img.shields.io/github/stars/auroraresearchlab/netbox-dns" alt="Stars Badge"/></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/network/members"><img src="https://img.shields.io/github/forks/auroraresearchlab/netbox-dns" alt="Forks Badge"/></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/pulls"><img src="https://img.shields.io/github/issues-pr/auroraresearchlab/netbox-dns" alt="Pull Requests Badge"/></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/issues"><img src="https://img.shields.io/github/issues/auroraresearchlab/netbox-dns" alt="Issues Badge"/></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/auroraresearchlab/netbox-dns?color=2b9348"></a>
<a href="https://github.com/auroraresearchlab/netbox-dns/blob/master/LICENSE"><img src="https://img.shields.io/github/license/auroraresearchlab/netbox-dns?color=2b9348" alt="License Badge"/></a>
</div>

## Features

* Manage zones (domains) you have.
* Manage nameservers for zones.
* Manage zone records.
* Assign tags to zones, nameservers and records.

## Requirements

* Netbox 3.0
* python 3.7

## Installation & Configuration

### Installation

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-dns
```

### Configuration

Add the plugin to the NetBox config. `~/netbox/configuration.py`

```python
PLUGINS = [
    "netbox_dns",
]
```

To permanently mount the plugin when updating netbox.

```
echo netbox-dns >> ~/netbox/local_requirements.txt
```

To add the required netbox-dns tables to your database run the following from your netbox directory:

```
./manage.py migrate
```

Full reference: [Using Plugins - NetBox Documentation](https://netbox.readthedocs.io/en/stable/plugins/)

## Screenshots

![Zones](https://raw.githubusercontent.com/auroraresearchlab/netbox-dns/main/media/zones.png)

![Zone Detail](https://raw.githubusercontent.com/auroraresearchlab/netbox-dns/main/media/zone-detail.png)

## Contribute

Contributions are always welcome! Please see: [contributing guide](CONTRIBUTING.md)

## License

MIT
