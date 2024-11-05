from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database import Base


class Element(Base):
    __tablename__ = "element"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, unique=True)
    emoji: Mapped[str] = mapped_column(Text)


class Pair(Base):
    __tablename__ = "pair"

    first_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Element.id), primary_key=True
    )
    second_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Element.id), primary_key=True
    )
    result_id: Mapped[int] = mapped_column(Integer, ForeignKey(Element.id))

    first: Mapped[Element] = relationship(Element, foreign_keys=[first_id])
    second: Mapped[Element] = relationship(Element, foreign_keys=[second_id])
    result: Mapped[Element] = relationship(Element, foreign_keys=[result_id])
