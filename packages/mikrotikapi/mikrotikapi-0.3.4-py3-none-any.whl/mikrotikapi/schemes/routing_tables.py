from pydantic import BaseModel, Field, AliasChoices, ConfigDict


class TableScheme(BaseModel):
    id: str = Field(
        default=None,
        validation_alias=AliasChoices(
            ".id",
            "id",
        ),
        serialization_alias=".id",
    )
    disabled: bool = Field(default=False)
    dynamic: bool = Field(default=None)
    invalid: bool = Field(default=False)
    name: str
    fib: str = Field(default="")

    @staticmethod
    def api_patch(_id=None):
        path = "/rest/routing/table"
        if _id:
            return f"{path}/{_id}"
        return path

    model_config = ConfigDict(populate_by_name=True)
