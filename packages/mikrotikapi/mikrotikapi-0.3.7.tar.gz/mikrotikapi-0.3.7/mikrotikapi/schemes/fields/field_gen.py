from typing import Any

from pydantic import Field, AliasChoices
from pydantic_core import PydanticUndefined

_Unset: Any = PydanticUndefined


def field_gen(
    default: Any = PydanticUndefined,
    *,
    name: str | None = _Unset,
    frozen=False,
):
    kebab_case = name.replace("_", "-")

    return Field(
        default=default,
        validation_alias=AliasChoices(
            kebab_case,
            name,
        ),
        serialization_alias=kebab_case,
        frozen=frozen,
    )
