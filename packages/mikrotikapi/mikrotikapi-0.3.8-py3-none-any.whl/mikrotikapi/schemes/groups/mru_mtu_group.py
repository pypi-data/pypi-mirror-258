from pydantic import BaseModel, Field, ConfigDict

from mikrotikapi.schemes.fields import field_gen


class MruMtuMrrugroup(BaseModel):
    max_mru: int = field_gen(1450, name="max_mru")
    max_mtu: int = field_gen(1450, name="max_mtu")
    mrru: str = Field("disabled")

    model_config = ConfigDict(populate_by_name=True)
