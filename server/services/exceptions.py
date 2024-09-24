from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE, HTTP_403_FORBIDDEN, \
    HTTP_409_CONFLICT

from application.exceptions import *


def add_exceptions(app):
    @app.exception_handler(BadRequestException)
    async def exception400_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"message": f"Oops! {exc.args} did something."})

    @app.exception_handler(NotFoundException)
    async def exception404_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"message": f"Oops! {exc.args} did something."})

    @app.exception_handler(NotAllowedException)
    async def exception403_handler(request: Request, exc: NotAllowedException):
        return JSONResponse(
            status_code= HTTP_403_FORBIDDEN,
            content={"message": f"Oops! {exc.args} did something."})

    @app.exception_handler(DeleteFailureException)
    async def exception406_handler(request: Request, exc: DeleteFailureException):
        return JSONResponse(
            status_code=HTTP_406_NOT_ACCEPTABLE,
            content={"message": f"Oops! {exc.args} did something."})

    @app.exception_handler(ConflictException)
    async def exception409_handler(request: Request, exc: ConflictException):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"message": f"Oops! {exc.args} did something."})