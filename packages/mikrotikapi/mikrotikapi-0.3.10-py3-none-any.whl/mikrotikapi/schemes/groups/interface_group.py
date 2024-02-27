from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components import Protocol
from mikrotikapi.schemes.fields import field_gen, in_interface, out_interface


class InterfaceGroup(
    Protocol,
    BaseModel,
):
    in_interface: str = in_interface
    out_interface: str = out_interface

    model_config = ConfigDict(populate_by_name=True)
