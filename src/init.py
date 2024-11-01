from csv import reader
from os import scandir
from os.path import join
from typing import Iterator

import config
from common import logger
from database import Base
from database import SessionLocal
from database import engine
from models import Element
from models import Pair


def _dump_entries(db: SessionLocal, path: str) -> Iterator[list[str]]:
    for entry in scandir(path):
        logger.debug("_dump_entry%s", entry)
        with open(entry.path, "r", encoding="utf-8") as file:
            csv = reader(file)
            next(csv)
            yield from csv
        db.commit()


def _dump_element(db: SessionLocal, element_path: str):
    logger.debug("_dump_element%s", locals())

    for row in _dump_entries(db, element_path):
        id_ = int(row[0])
        if id_ != 1:
            element = Element(id=id_, text=row[1], emoji=row[2])
            db.add(element)


def _dump_pair(db: SessionLocal, pair_path: str):
    logger.debug("_dump_pair%s", locals())

    for row in _dump_entries(db, pair_path):
        result_id = int(row[2])
        if result_id != 1:
            pair = Pair(
                first_id=int(row[0]), second_id=int(row[1]), result_id=result_id
            )
            db.add(pair)


def dump_database(data_path: str = config.DATA_PATH):
    logger.debug("dump_database%s", locals())

    load_database()
    db = SessionLocal()

    _dump_element(db, join(data_path, "element"))
    _dump_pair(db, join(data_path, "pair"))

    close_database()


def load_database():
    Base.metadata.create_all(engine)


def close_database():
    engine.dispose()


def main():
    dump_database()


if __name__ == "__main__":
    main()
