from datetime import datetimefrom pydantic import BaseModel, Field, field_validator, IPvAnyAddressclass SecretScheme(BaseModel):    id: str = Field(alias=".id")    caller_id: str = Field(alias="caller-id")    disabled: bool    ipv6_routes: str = Field(alias="ipv6-routes")    last_caller_id: str = Field(        default=None, alias="last-caller-id", frozen=True    )    last_disconnect_reason: str = Field(        default=None, alias="last-disconnect-reason", frozen=True    )    last_logged_out: datetime = Field(alias="last-logged-out", frozen=True)    limit_bytes_in: int = Field(alias="limit-bytes-in")    limit_bytes_out: int = Field(alias="limit-bytes-out")    name: str    password: str    profile: str    routes: str    service: str    @staticmethod    def api_patch():        return "/rest/ppp/secret"    class Config:        populate_by_name = True