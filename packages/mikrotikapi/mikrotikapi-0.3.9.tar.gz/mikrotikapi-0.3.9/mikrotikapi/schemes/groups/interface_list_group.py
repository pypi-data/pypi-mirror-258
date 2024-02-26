from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components import Protocol
from mikrotikapi.schemes.fields import field_gen


class InterfaceListGroup(
    Protocol,
    BaseModel,
):
    in_interface_list: str = field_gen("", name="in_interface")
    out_interface_list: str = field_gen("", name="out_interface")

    model_config = ConfigDict(populate_by_name=True)
