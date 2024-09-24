import os
from enum import Enum

from sqlalchemy import create_engine, MetaData, text, Table
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.db')
SQLALCHEMY_DATABASE_URL = f"sqlite+pysqlite:///{db_path}" # infrastructure/db.db
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine_async = create_async_engine(f"sqlite+aiosqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalAsync = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_async, expire_on_commit=False)

metadata = MetaData()
metadata.reflect(engine)

def get_db_session(in_memory=False):
    return metadata, SessionLocal, SessionLocalAsync

with SessionLocal() as conn:
    a = conn.execute(text("SELECT * FROM user"))
    print(a.all())

with engine.connect() as conn:
    a = conn.execute(text("SELECT * FROM user"))
    print(a.all())

    users = metadata.tables['user']
    b = conn.execute(users.select())
    # b2 = conn.execute(users.delete().where(users.c.email == "some_other2"))
    # b1 = conn.execute(users.insert().values(userid="temp2", email="some_other2", password="some_other"))
    print(b.all())
    print(conn.execute(users.select().where(users.c.username == "username")).first())


class Database(object):
    Session = SessionLocal
    SessionAsync = SessionLocalAsync

    class Tables(object):
        Users = metadata.tables["user"]
        Sessions = metadata.tables["session"]
        Claims = metadata.tables["claim"]
