from pydantic import (
    Field,
    AliasChoices,
)

log_prefix_field = Field(
    default="",
    validation_alias=AliasChoices(
        "log-prefix",
        "log_prefix",
    ),
    serialization_alias="log-prefix",
)
