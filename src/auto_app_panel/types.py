from typing import Literal, Protocol

import pydantic


class Parameter(pydantic.BaseModel):
    name: str
    type: Literal["string", "integer", "number"]
    default_value: str | float | int | None = None
    description: str | None = None


class ParameterExtractor(Protocol):
    def extract_parameters(self, file_path: str) -> list[Parameter]:
        ...
