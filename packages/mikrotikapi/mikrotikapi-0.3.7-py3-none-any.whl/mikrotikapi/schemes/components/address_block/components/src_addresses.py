from pydantic import (
    BaseModel,
    Field,
    IPvAnyNetwork,
    ConfigDict,
    AliasChoices,
    field_validator,
    field_serializer,
)

from mikrotikapi.utils.split_and_join import (
    split_ip_network_values,
    join_ip_network_values,
)


class SrcAddresses(BaseModel):
    src_addresses: list[IPvAnyNetwork | str] = Field(
        None,
        avalidation_alias=AliasChoices(
            "src-addresses",
            "src_addresses",
        ),
        serialization_alias="src-addresses",
    )

    @field_validator("src_addresses", mode="before")
    def src_addresses_validate(cls, v) -> list:
        return split_ip_network_values(v)

    @field_serializer("src_addresses")
    def src_addresses_serialize(self, to_addresses: list, _info):
        return join_ip_network_values(to_addresses)

    model_config = ConfigDict(populate_by_name=True)
