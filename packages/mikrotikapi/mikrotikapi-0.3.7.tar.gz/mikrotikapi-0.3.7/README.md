[![Python package](https://github.com/goltsevnet/MikrotikApi/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/goltsevnet/MikrotikApi/actions/workflows/python-package.yml)


# MikrotikApi

MikrotikApi is a project intended for managing RouterOS.

## Installation

MikrotikApi was developed using the [Python](https://www.python.org/downloads/) programming language. You can install the project's dependencies with pip:

```shell
pip install mikrotikapi
```

Or using poetry:

```shell
poetry add mikrotikapi
```

## Usage

```python
import os
from mikrotikapi import ROSApi
from mikrotikapi.schemes import NatScheme
from mikrotikapi.schemes.fields.action import ActionController
from mikrotikapi.schemes.fields.chain import ChainController



your_login = os.getenv("your_login")
your_password = os.getenv("your_password")
mikrotik_address = os.getenv("mikrotik_address") # look setting www-ssl port
mikrotik_port = os.getenv("mikrotik_port")

api = ROSApi(
    url=mikrotik_address,
    username=your_login,
    password=your_password,
)

nat = NatScheme(
    src_address="172.22.8.0/30",
    chain="srcnat",
    action="masquerade",
)

# NatScheme(to_addresses=None, chain=<ChainController.srcnat: 'srcnat'>,
# dst_addresses=None, dst_address=None, src_addresses=None, src_address=IPv4Network
# ('172.22.8.0/30'), action=<ActionController.masquerade: 'masquerade'>, 
# to_ports=None, protocol=None, id=None, bytes=0, comment='', disabled=False, 
# dst_port=None, dynamic=None, invalid=None, log=False, log_prefix='', packets=None,
# routing_mark=None, in_interface='', out_interface='')

# or...

nat = NatScheme(
    src_address="172.22.8.0/30",
    chain=ChainController.srcnat,
    action=ActionController.masquerade,
)


# or...

nat = NatScheme()
nat.src_address = "172.22.8.0/30"
nat.chain = ChainController.srcnat
nat.action = ActionController.masquerade
nat.comment = "first comment"

# Всегда результат один:

nat.src_address

# IPv4Network('172.22.8.0/30')


api.objects(NatScheme).create(nat)


# or...

all_nats = api.objects(NatScheme).all()


```

