from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    
    return create_engine(URL(**settings.DATABASE))


def create_cafes_table(engine):

    DeclarativeBase.metadata.create_all(engine)


class Cafes(DeclarativeBase):

    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    address = Column('address', String)
