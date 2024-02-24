from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.components.address_block.components import (
    SrcAddress,
    SrcAddresses,
    DstAddress,
    DstAddresses,
)
from mikrotikapi.schemes.components.chain_block import ChainBlock


class SrcAddressBlock(
    SrcAddress,
    SrcAddresses,
    DstAddress,
    DstAddresses,
    ChainBlock,
    BaseModel,
):

    model_config = ConfigDict(populate_by_name=True)
