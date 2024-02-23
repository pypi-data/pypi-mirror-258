from pydantic import Field, AliasChoices

routing_mark_field = Field(
    default="",
    validation_alias=AliasChoices(
        "routing-mark",
        "routing_mark",
    ),
    serialization_alias="routing-mark",
)
