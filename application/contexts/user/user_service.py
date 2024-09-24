from typing import Union

from sqlalchemy import select, Table, and_, or_, insert
from sqlalchemy.orm import Session

from application.exceptions import NotFoundException, NotAllowedException
from application.services import get_uuid, get_now_ts
from server.services.secuity import get_jwt


class UserService(object):
    def __init__(self, db):
        self.meta, self.db, self.db_async = db

    def create_token(self, username_or_email: str, password: str, device: str) -> Union[str, None]:
        users = self.meta.tables['user']
        sessions = self.meta.tables['session']
        claims = self.meta.tables['claim']
        with (self.db() as session):
            q_user = select(users.c.userid, users.c.suspendargs).where(and_(or_(users.c.username == username_or_email, users.c.email == username_or_email), users.c.password == password))
            user = session.execute(q_user).first()
            if user is None:
                raise NotFoundException("User not found", "")

            if user.suspendargs is not None:
                raise NotAllowedException("Account is Suspended", "")

            q_get_session = select(sessions).where(and_(sessions.c.userid==user.userid, sessions.c.terminated_ts == None))
            ses = session.execute(q_get_session).first()
            if not ses:
                stmt = insert(sessions).values(sessionid=get_uuid(), userid=user.userid, device=device, created_ts=get_now_ts())
                session.execute(stmt)
                session.commit()

            claims = session.execute(select(claims)).all()
            # claims = session.execute(select(claims.c.claimtype, claims.c.claimvalue).where(and_(claims.c.userid==user.userid, claims.c.revoked_ts == None))).all()
            print("claims are", claims)

            token = get_jwt({"device": device})
            return token



    def update_token(self) -> Union[str, None]:
        pass

    async def terminate_token(self, token: str, device: str):
        sessions = self.meta.tables['session']
        print(f"Here is logout function the token is {token} and device is {device}")