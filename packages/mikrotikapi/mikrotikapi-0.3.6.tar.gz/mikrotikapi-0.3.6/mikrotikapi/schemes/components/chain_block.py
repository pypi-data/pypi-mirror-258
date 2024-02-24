from pydantic import BaseModel

from mikrotikapi.schemes.fields.chain import ChainController, chain


class ChainBlock(BaseModel):
    chain: ChainController = chain
