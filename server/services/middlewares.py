import time
from http import HTTPStatus

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from server.routes import PG_LOGIN, PG_INDEX
from server.services.secuity import get_claims


class ApplicationMW(object):
    def __init__(self, app: FastAPI, db):
        self.db = db
        self.app = app

    def add_middlewares(self):
        @self.app.middleware("http")
        async def show_request_process_time(request: Request, call_next) -> Response:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        @self.app.middleware("http")
        async def inject_token_in_request(request: Request, call_next) -> Response:
            token = request.cookies.get("token")
            request.state.token = token
            response = await call_next(request)
            return response
