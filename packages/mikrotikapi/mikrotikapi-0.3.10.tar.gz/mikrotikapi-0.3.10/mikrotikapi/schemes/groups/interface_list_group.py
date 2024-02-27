from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components import Protocol
from mikrotikapi.schemes.fields import in_interface_list, out_interface_list


class InterfaceListGroup(
    Protocol,
    BaseModel,
):
    in_interface_list: str = in_interface_list
    out_interface_list: str = out_interface_list

    model_config = ConfigDict(populate_by_name=True)
