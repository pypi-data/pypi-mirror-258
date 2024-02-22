from __future__ import annotationsfrom pydantic import (    BaseModel,    Field,    field_validator,    IPvAnyAddress,    IPvAnyNetwork,)class NatScheme(BaseModel):    id: str = Field(default=None, alias=".id")    action: str = Field(default=None)    bytes: int = Field(default=None, frozen=True, exclude=True)    chain: str = Field(default=None)    dynamic: bool = Field(default=None, frozen=True, exclude=True)    invalid: bool = Field(default=None, frozen=True, exclude=True)    packets: str = Field(default=None, frozen=True, exclude=True)    out_interface: str = Field(default=None, alias="out-interface")    src_address: IPvAnyNetwork | str = Field(default=None, alias="src-address")    to_addresses: IPvAnyAddress = Field(        default=None, alias="to-addresses", frozen=True    )    @staticmethod    def api_patch(_id=None):        if _id:            return f"/rest/ip/firewall/nat/{_id}"        return "/rest/ip/firewall/nat"    class Config:        populate_by_name = True