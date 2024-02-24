from enum import Enum
from pydantic import Field


class ActionController(str, Enum):
    accept = "accept"
    dst_nat = "dst-nat"
    add_dst_to_address_list = "add dst to address list"
    add_sre_to_address_list = "add sre to address list"
    endpoint_independent_nat = "endpoint-independent-nat"
    jump = "jump"
    log = "log"
    masquerade = "masquerade"
    netmap = "netmap"
    passthrough = "passthrough"
    redirect = "redirect"
    return_ = "return"
    same = "same"
    src_nat = "src-nat"


action = Field(default=ActionController.accept)
