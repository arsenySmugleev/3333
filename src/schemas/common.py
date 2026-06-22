from typing import Annotated, Optional

from pydantic import Field

NameStr = Annotated[str, Field(min_length=1, max_length=200, strip_whitespace=True)]
OptionalNameStr = Annotated[
    Optional[str],
    Field(default=None, min_length=1, max_length=200, strip_whitespace=True),
]
PolicyNumber = Annotated[int, Field(gt=0)]
OptionalPolicyNumber = Annotated[Optional[int], Field(default=None, gt=0)]
