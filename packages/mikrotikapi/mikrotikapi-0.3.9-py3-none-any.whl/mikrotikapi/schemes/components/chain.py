from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.fields.chain import ChainController, chain


class Chain(BaseModel):
    chain: ChainController | str = chain
    model_config = ConfigDict(populate_by_name=True)
