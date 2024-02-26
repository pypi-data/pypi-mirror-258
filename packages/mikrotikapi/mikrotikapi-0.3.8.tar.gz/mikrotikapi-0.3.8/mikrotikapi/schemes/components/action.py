from pydantic import BaseModel, ConfigDict

from mikrotikapi.schemes.fields.action import ActionController, action


class Action(BaseModel):
    action: ActionController | str = action

    model_config = ConfigDict(populate_by_name=True)
