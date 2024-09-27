from typing import Union

from sqlalchemy import select, and_, or_, insert, update

from application.exceptions import NotFoundException, NotAllowedException
from application.services import get_uuid, get_now_ts
from infrastructure.repository import Database
from server.services.secuity import get_jwt, get_claims


class UserService(object):
    def __init__(self, db: Database):
        self.db = db

    def create_token(self, username_or_email: str, password: str, device: str) -> str:
        users = self.db.tbl_users()
        sessions = self.db.Tables.Sessions
        claims = self.db.Tables.Claims
        with (self.db.Session() as session):
            q_user = select(users.c.userid, users.c.suspendargs).where(and_(or_(users.c.username == username_or_email, users.c.email == username_or_email), users.c.password == password))
            user = session.execute(q_user).first()
            if user is None:
                raise NotFoundException("User not found", "")

            if user.suspendargs is not None:
                raise NotAllowedException("Account is Suspended", user.suspendargs)

            q_get_session = select(sessions).where(and_(sessions.c.userid==user.userid, sessions.c.device==device, sessions.c.terminated_ts == None))
            ses = session.execute(q_get_session).first()
            if not ses:
                stmt = insert(sessions).values(sessionid=get_uuid(), userid=user.userid, device=device, created_ts=get_now_ts())
                session.execute(stmt)
                session.commit()
            ses = session.execute(q_get_session).first()

            claims_ = session.execute(select(claims.c.claimtype, claims.c.claimvalue).where(and_(claims.c.userid==user.userid, claims.c.revoked_ts == None))).all()
            claims__ = {"session": ses.sessionid, "device": device}
            for c, d in claims_:
                claims__[c] = d

            token = get_jwt(claims__)
            return token
        raise NotImplementedError


    async def update_token(self, token: str, device: str) -> str:
        claims = await self.get_recent_claims(token, device)
        if not claims:
            raise NotFoundException("", "")

        return get_jwt(claims)

    async def terminate_token(self, session_id: str, device: str) -> None:
        sessions = self.db.Tables.Sessions
        if not await self.get_recent_claims(session_id, device):
            raise NotFoundException("", "")

        async with (self.db.SessionAsync() as session):
            await session.execute(update(sessions).where(and_(sessions.c.sessionid==session_id, sessions.c.device==device)).values(terminated_ts=get_now_ts()))
            await session.commit()
            return

    async def get_recent_claims(self, session_id: str, device: str) -> Union[dict, None]:
        sessions = self.db.Tables.Sessions
        users = self.db.Tables.Users
        claims = self.db.Tables.Claims
        async with (self.db.SessionAsync() as session):
            stmt = select(claims.c.claimtype, claims.c.claimvalue).join(users, users.c.userid == claims.c.userid).join(sessions, sessions.c.userid == users.c.userid).where(
                and_(
                    claims.c.revoked_ts == None,
                    users.c.suspendargs == None,
                    sessions.c.terminated_ts == None,
                    sessions.c.sessionid == session_id,
                    sessions.c.device == device))

            claims_ = await session.execute(stmt)
            claims_ = claims_.all()
            if len(claims_) > 0:
                claims__ = {"session": session_id, "device": device}
                for c, d in claims_:
                    claims__[c] = d
                return claims__

            return None