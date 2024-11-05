from typing import Literal

from pydantic import BaseModel

from models import Element


class Result(BaseModel):
    result: str
    emoji: str
    isNew: Literal[False] = False

    @classmethod
    def from_element(cls, element: Element):
        return cls(result=element.text, emoji=element.emoji)


RESULT_NOTHING = Result(result="Nothing", emoji="")
