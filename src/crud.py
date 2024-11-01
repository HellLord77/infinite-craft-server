from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Element
from models import Pair
from schemas import Result


def get_result(first: str, second: str, db: Session = Depends(get_db)) -> Result:
    result = "Nothing"
    emoji = ""
    first_id = db.query(Element.id).filter(Element.text == first).first()
    if first_id is not None:
        second_id = db.query(Element.id).filter(Element.text == second).first()
        if second_id is not None:
            if first_id[0] > second_id[0]:
                first_id, second_id = second_id, first_id
            pair = (
                db.query(Pair)
                .filter(Pair.first_id == first_id[0], Pair.second_id == second_id[0])
                .first()
            )
            if pair is not None:
                result = pair.result.text
                emoji = pair.result.emoji
    return Result(result=result, emoji=emoji)
