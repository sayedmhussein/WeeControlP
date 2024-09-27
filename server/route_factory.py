
from typing import Annotated, Union, Final

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.params import Cookie
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from server.routers.user_router import UserContext
from server.routes import PG_INDEX, V2_ESSENTIAL


class RoutingFactory(object):
    def __init__(self, app: FastAPI, db):
        self.app = app
        self.db = db

    def setup_routes(self):
        index_route(self.app)
        UserContext(self.app, self.db).setup_routing()

    async def setup_routes_async(self):
        await UserContext(self.app, self.db).setup_routing_async()


def index_route(app: FastAPI):
    @app.get(PG_INDEX, response_class=HTMLResponse)
    def index(request: Request, ads_id: Annotated[str | None, Cookie()] = None, token: Annotated[str | None, Cookie()] = None):
        templates = Jinja2Templates(directory="templates")
        response = templates.TemplateResponse(request=request, name="hello.html", context={"person": ads_id})
        response.set_cookie("ads_id", "hello world")
        return response

    @app.get(V2_ESSENTIAL+"/{item_id}")
    async def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}






