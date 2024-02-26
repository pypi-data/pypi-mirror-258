from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components import (
    SrcAddress,
    SrcAddresses,
    DstAddress,
    DstAddresses,
    Chain,
)


class AddressMatchGroup(
    SrcAddress,
    SrcAddresses,
    DstAddress,
    DstAddresses,
    Chain,
    BaseModel,
):
    model_config = ConfigDict(populate_by_name=True)
