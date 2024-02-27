from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    field_serializer,
)

from mikrotikapi.schemes.fields.to_ports import to_ports
from mikrotikapi.utils.split_and_join import join_values


class ToPorts(BaseModel):
    to_ports: int | str | list[int] = to_ports

    @field_validator("to_ports", mode="before")
    def validate_to_ports(cls, to_ports_: str | int):
        ports = str(to_ports_).split("-")

        if len(ports) == 1:
            port = int(ports[0])
            if not (0 <= port <= 65535):
                raise ValueError("Port must be in range 0-65535")
            return port

        elif len(ports) == 2:
            port_start, port_end = map(int, ports)
            if not (0 <= port_start <= 65535) or not (0 <= port_end <= 65535):
                raise ValueError("Ports must be in range 0-65535")
            if port_start > port_end:
                raise ValueError(
                    "Invalid range. Start of range cannot be greater than end."
                )
            return [port_start, port_end]

        else:
            raise ValueError("Invalid port value or range format.")

    @field_serializer("to_ports")
    def to_ports_serialize(self, v: list, _info):
        return join_values(v, delimiter="-")

    model_config = ConfigDict(populate_by_name=True)
