from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.fields.protocol import ProtocolController, protocol


class Protocol(BaseModel):
    protocol: ProtocolController = protocol

    model_config = ConfigDict(populate_by_name=True)
