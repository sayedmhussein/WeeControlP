import time

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

from application.contexts.user.user_service import UserService
from infrastructure.repository import Database
from server.services.secuity import get_claims


class ApplicationMW(object):
    def __init__(self, app: FastAPI, db):
        self.db = db
        self.app = app

    def add_middlewares(self):
        @self.app.middleware("http")
        async def log_request_response_data(request: Request, call_next) -> Response:
            response = await call_next(request)
            token, device, claims = get_token_device_claims(request)
            if claims is not None:
                await UserService(Database()).log_activity(claims["session"], str(request.url), request.method, response.status_code)
            return response

        @self.app.middleware("http")
        async def show_request_process_time(request: Request, call_next) -> Response:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        @self.app.middleware("http")
        async def inject_token_in_request(request: Request, call_next) -> Response:
            token, device, _ = get_token_device_claims(request)
            request.state.token = token
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

def get_token_device_claims(request: Request):
    token = request.cookies.get("token")

    device = ";".join(filter(None, [
        request.headers.get("Device"),
        request.headers.get("Host"),
        request.headers.get("User-Agent")]))

    claims = get_claims(token)

    return token, device, claims