from pydantic import (
    BaseModel,
    Field,
    IPvAnyNetwork,
    ConfigDict,
    AliasChoices,
)


class DstAddress(BaseModel):
    dst_address: IPvAnyNetwork | str = Field(
        default=None,
        validation_alias=AliasChoices(
            "dst-address",
            "dst_address",
        ),
        serialization_alias="dst-address",
    )

    model_config = ConfigDict(populate_by_name=True)
