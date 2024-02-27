from pydantic import (
    Field,
    AliasChoices,
)

id_field = Field(
    default=None,
    validation_alias=AliasChoices(
        ".id",
        "id",
    ),
    serialization_alias=".id",
)
