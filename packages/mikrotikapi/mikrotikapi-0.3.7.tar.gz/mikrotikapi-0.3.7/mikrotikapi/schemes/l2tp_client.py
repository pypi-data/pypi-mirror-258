from __future__ import annotations


from pydantic import (
    BaseModel,
    Field,
    field_validator,
    IPvAnyAddress,
    ConfigDict,
    field_serializer,
)

from mikrotikapi.schemes.fields import (
    comment_field,
    id_field,
    field_gen,
    running_field,
)
from mikrotikapi.utils.split_and_join import split_values, join_values


class L2TPClientScheme(BaseModel):
    id: str = id_field
    add_default_route: bool = field_gen(False, name="add_default_route")
    allow: list = Field(default=[])
    allow_fast_path: bool = field_gen(False, name="allow_fast_path")
    comment: str = comment_field
    connect_to: IPvAnyAddress | str = field_gen(None, name="connect_to")
    dial_on_demand: bool = field_gen(False, name="dial_on_demand")
    disabled: bool = Field(default=False)
    ipsec_secret: str = field_gen("", name="ipsec_secret")
    keepalive_timeout: int = field_gen(60, name="keepalive_timeout")
    l2tp_proto_version: str = field_gen("l2tpv2", name="l2tp_proto_version")
    l2tpv3_digest_hash: str = field_gen("md5", name="l2tpv3_digest_hash")
    max_mru: int = field_gen(1450, name="max_mru")
    max_mtu: int = field_gen(1450, name="max_mtu")
    mrru: str = Field(default="disabled")
    name: str
    password: str
    profile: str = Field(default="default-encryption")
    running: bool = running_field
    use_ipsec: bool = field_gen(False, name="use_ipsec")
    use_peer_dns: str = field_gen("no", name="use_peer_dns")
    user: str = Field(default="")

    @field_validator("allow", mode="before")
    def allow_validate(cls, allow) -> list:
        return split_values(allow)

    @field_serializer("allow")
    def serialize_allow(self, allow: list, _info):
        return join_values(allow)

    @staticmethod
    def api_patch(_id=None):
        path = "/rest/interface/l2tp-client"
        if _id:
            return f"{path}/{_id}"
        return path

    @field_serializer("keepalive_timeout", "max_mru", "max_mtu")
    def serialize_dt(self, v, _info):
        return str(v)

    model_config = ConfigDict(populate_by_name=True)
