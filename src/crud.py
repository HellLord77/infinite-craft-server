from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

from models import Element
from models import Pair
from schemas import RESULT_NOTHING
from schemas import Result


def get_result(pair: tuple[str, str], session: Session) -> Result:
    pair = sorted(pair)
    first = aliased(Element)
    second = aliased(Element)
    result = aliased(Element)
    # noinspection PyTypeChecker
    result = session.scalar(
        select(result)
        .join(first, Pair.first)
        .join(second, Pair.second)
        .join(result, Pair.result)
        .where(first.text == pair[0], second.text == pair[1])
    )
    return RESULT_NOTHING if result is None else Result.from_element(result)
