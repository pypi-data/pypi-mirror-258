from enum import Enum

from mikrotikapi.schemes.fields import field_gen


class InInterfaceListController(str, Enum):
    all = "all"
    dynamic = "dynamic"
    none = "none"
    static = "static"


in_interface_list: InInterfaceListController = field_gen(
    None, "in_interface_list"
)
