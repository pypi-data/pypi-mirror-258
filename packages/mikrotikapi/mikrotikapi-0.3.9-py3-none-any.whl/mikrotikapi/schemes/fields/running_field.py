from pydantic import Field

running_field = Field(
    None,
    exclude=True,
    frozen=True,
)
