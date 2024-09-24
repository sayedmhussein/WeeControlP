
from typing import Annotated, Union, Final

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.params import Cookie

from server.routers.user_router import UserContext
from server.routes import PG_INDEX


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
    @app.get(PG_INDEX)
    def index(ads_id: Annotated[str | None, Cookie()] = None, token: Annotated[str | None, Cookie()] = None):
        content = {"message": f"Come to the dark side, we have cookies {ads_id}, {token}"}
        response = JSONResponse(content=content)
        response.set_cookie("ads_id", "hello world")
        return response

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}






