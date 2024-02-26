from enum import Enum

from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components import Protocol
from mikrotikapi.schemes.fields import field_gen


class NoMarkController(str, Enum):
    no_mark = "no-mark"


class MarkGroup(
    Protocol,
    BaseModel,
):
    packet_mark: NoMarkController | str = field_gen(None, "packet-mark")
    connection_mark: NoMarkController | str = field_gen(
        None, "connection-mark"
    )
    routing_mark: NoMarkController | str = field_gen(None, "routing-mark")

    model_config = ConfigDict(populate_by_name=True)
