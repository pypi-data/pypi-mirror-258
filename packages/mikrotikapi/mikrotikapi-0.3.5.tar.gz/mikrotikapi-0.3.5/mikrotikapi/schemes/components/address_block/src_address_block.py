from __future__ import annotations

from pydantic import (
    BaseModel,
    Field,
    IPvAnyNetwork,
    ConfigDict,
    AliasChoices,
)

from mikrotikapi.schemes.components.address_block.components import (
    SrcAddress,
    SrcAddresses,
    DstAddress,
)


class SrcAddressBlock(
    SrcAddress,
    SrcAddresses,
    DstAddress,
    BaseModel,
):

    dst_addresses: list[IPvAnyNetwork] = Field(
        default=None,
        validation_alias=AliasChoices(
            "dst-addresses",
            "dst_addresses",
        ),
        serialization_alias="dst-addresses",
    )

    model_config = ConfigDict(populate_by_name=True)
