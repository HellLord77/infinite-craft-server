from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import relationship

from database import Base


class Element(Base):
    __tablename__ = "element"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    text = Column(Text, nullable=False, unique=True)
    emoji = Column(Text, nullable=False)

class Pair(Base):
    __tablename__ = "pair"

    first_id = Column(Integer, ForeignKey("element.id"), primary_key=True, nullable=False)
    second_id = Column(Integer, ForeignKey("element.id"), primary_key=True, nullable=False)
    result_id = Column(Integer, ForeignKey("element.id"), nullable=False)

    # noinspection PyTypeChecker
    first = relationship("Element", foreign_keys=[first_id])
    # noinspection PyTypeChecker
    second = relationship("Element", foreign_keys=[second_id])
    # noinspection PyTypeChecker
    result = relationship("Element", foreign_keys=[result_id])
