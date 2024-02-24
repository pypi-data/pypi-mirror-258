from pydantic import (
    BaseModel,
    Field,
    IPvAnyNetwork,
    ConfigDict,
    AliasChoices,
)


class SrcAddresses(BaseModel):
    src_addresses: list[IPvAnyNetwork | str] = Field(
        default=None,
        avalidation_alias=AliasChoices(
            "src-addresses",
            "src_addresses",
        ),
        serialization_alias="src-addresses",
    )

    model_config = ConfigDict(populate_by_name=True)
