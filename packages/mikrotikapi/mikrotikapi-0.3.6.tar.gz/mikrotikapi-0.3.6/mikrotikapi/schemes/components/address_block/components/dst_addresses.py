from __future__ import annotations

from pydantic import (
    BaseModel,
    Field,
    IPvAnyNetwork,
    ConfigDict,
    AliasChoices,
)


class DstAddresses(BaseModel):

    dst_addresses: list[IPvAnyNetwork | str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "dst-addresses",
            "dst_addresses",
        ),
        serialization_alias="dst-addresses",
    )

    model_config = ConfigDict(populate_by_name=True)
