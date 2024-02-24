from pydantic import (
    BaseModel,
    IPvAnyNetwork,
    ConfigDict,
    field_validator,
    field_serializer,
    IPvAnyAddress,
)

from mikrotikapi.schemes.components import SrcAddressBlock
from mikrotikapi.schemes.fields import field_gen
from mikrotikapi.utils.split_and_join import (
    split_ip_network_values,
    join_ip_network_values,
)


class ToAddresses(SrcAddressBlock, BaseModel):
    to_addresses: list[IPvAnyAddress | IPvAnyNetwork | str] = field_gen(
        "to_addresses"
    )

    @field_validator("to_addresses", mode="before")
    def to_addresses_validate(cls, v) -> list:
        return split_ip_network_values(v)

    @field_serializer("to_addresses")
    def to_addresses_serialize(self, to_addresses: list, _info):
        return join_ip_network_values(to_addresses)

    model_config = ConfigDict(populate_by_name=True)
