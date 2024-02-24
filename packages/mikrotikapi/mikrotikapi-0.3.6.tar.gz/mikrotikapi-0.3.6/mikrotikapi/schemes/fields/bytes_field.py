from pydantic import Field

bytes_field = Field(default=0, frozen=True, exclude=True)
