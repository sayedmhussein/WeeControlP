import time

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

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
            device = ";".join(filter(None, [
                request.headers.get("Device"),
                request.headers.get("Host"),
                request.headers.get("User-Agent")]))
            request.state.device = device

            claims = get_claims(token)
            if claims is not None:
                request.state.token = token
                claims = get_claims(token)
                request.state.session = claims["session"]
                request.state.device = claims["device"]

                if device != claims["device"]:
                    response = JSONResponse("User don't have right to access the resource", status_code=HTTP_403_FORBIDDEN)
                    return response

            response = await call_next(request)
            return response
