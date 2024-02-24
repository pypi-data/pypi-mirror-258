from pydantic import (
    BaseModel,
    IPvAnyNetwork,
    ConfigDict,
    field_validator,
)

from mikrotikapi.schemes.fields import field_gen


class SrcAddress(BaseModel):
    src_address: IPvAnyNetwork | str = field_gen("src_address", default=None)

    @field_validator("src_address", mode="before")
    def src_address_validate(cls, v):
        if isinstance(v, str) and v == "":
            return None
        return v

    model_config = ConfigDict(populate_by_name=True)
