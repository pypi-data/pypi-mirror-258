from pydantic import BaseModel

from mikrotikapi.schemes.fields.action import ActionController, action


class ActionBlock(BaseModel):
    action: ActionController = action
