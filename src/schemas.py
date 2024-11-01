from typing import Literal

from pydantic import BaseModel


class Result(BaseModel):
    result: str
    emoji: str
    isNew: Literal[False] = False
