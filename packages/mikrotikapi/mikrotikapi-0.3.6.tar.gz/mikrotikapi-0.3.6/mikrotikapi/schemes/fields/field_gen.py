from pydantic import Field, AliasChoices


def field_gen(name: str, default="", frozen=False):
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
