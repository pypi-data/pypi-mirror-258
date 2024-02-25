from pydantic import (
    BaseModel,
    IPvAnyNetwork,
    ConfigDict,
)

from mikrotikapi.schemes.fields import field_gen


class SrcAddress(BaseModel):
    src_address: IPvAnyNetwork | str = field_gen(None, name="src_address")

    model_config = ConfigDict(populate_by_name=True)
