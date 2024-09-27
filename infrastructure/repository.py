import os

from sqlalchemy import create_engine, MetaData, text, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session, Session

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.db')
SQLALCHEMY_DATABASE_URL = f"sqlite+pysqlite:///{db_path}" # infrastructure/db.db
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 5})
engine_async = create_async_engine(f"sqlite+aiosqlite:///{db_path}", connect_args={"check_same_thread": False, "timeout": 5})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalAsync = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_async, expire_on_commit=False)

metadata = MetaData()
metadata.reflect(engine)


def get_session():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()

class Database(object):
    Session: sessionmaker[Session] = SessionLocal
    SessionAsync: async_sessionmaker[AsyncSession] = SessionLocalAsync

    class Tables(object):
        Addresses = metadata.tables["address"]
        Contacts = metadata.tables["contact"]
        Offices = metadata.tables["office"]

        Users = metadata.tables["user"]
        UserSessions = metadata.tables["usersession"]
        UserNotifications = metadata.tables["usernotification"]
        UserLogs = metadata.tables["userlog"]
        UserClaims = metadata.tables["userclaim"]


def run_query():
    with SessionLocal() as conn:
        stmt = update(Database.Tables.Users).values(salt=b'\xa6\xf5]Y8\xb2\xf3L\x10c\x92t\xa8\xb2J\x00', password=b'6\x1ew\x8d\x18\x84Tv)\x8a\xf8\xfd\xc0\xba\xd5\x8b\\\x9a\xb4S?9)\xf9\x0e\x9f\xae\xf2\xfd\xe7\x1e\xd0')
        a = conn.execute(stmt)
        conn.commit()

    with SessionLocal() as conn:
        a = conn.execute(text("SELECT * FROM user"))
        print(a.all())

    with engine.connect() as conn:
        a = conn.execute(text("SELECT * FROM user"))
        print(a.all())

        users = metadata.tables['user']
        b = conn.execute(users.select())
        print(b.all())
        print(conn.execute(users.select().where(users.c.username == "username")).first())

# run_query()