from enum import Enum
from pydantic import Field

from mikrotikapi.schemes.fields import field_gen


class OutInterfaceListController(str, Enum):
    all = "all"
    dynamic = "dynamic"
    none = "none"
    static = "static"


out_interface_list: OutInterfaceListController = field_gen(
    None,
    "out_interface_list",
)
