from pydantic import Field

running_field = Field(
    default=None,
    exclude=True,
    frozen=True,
)
