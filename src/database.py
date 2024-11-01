from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG_SQLALCHEMY)
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

Base = declarative_base()
