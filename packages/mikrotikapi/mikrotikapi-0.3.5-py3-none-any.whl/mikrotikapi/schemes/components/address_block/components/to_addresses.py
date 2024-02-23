from pydantic import (
    BaseModel,
    IPvAnyNetwork,
    ConfigDict,
    field_validator,
)

from mikrotikapi.schemes.components import SrcAddressBlock
from mikrotikapi.schemes.fields import field_gen


class ToAddresses(SrcAddressBlock, BaseModel):
    to_addresses: list[IPvAnyNetwork] = field_gen("to_addresses", frozen=True)

    @field_validator("to_addresses", mode="before")
    def allow_validate(cls, v) -> list:
        if isinstance(v, str):
            addresses = v.split(",")
            return [IPvAnyNetwork(address) for address in addresses]
        else:
            return v

    model_config = ConfigDict(populate_by_name=True)
