import json
from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from server.routers.user_router import UserContext
from server.routers.webpage_router import add_webpages
from server.routes import V2_ESSENTIAL, ClaimTypes


class RoutingFactory(object):
    def __init__(self, app: FastAPI, db):
        self.app = app
        self.db = db

    def setup_routes(self):
        add_webpages(self.app, self.db)
        add_essentials(self.app)

    async def setup_routes_async(self):
        await UserContext(self.app, self.db).setup_routing()


def add_essentials(app: FastAPI):
    @app.get(V2_ESSENTIAL+"/{name}", tags=["Essential"])
    async def read_item(name: str, q: Union[str, None] = None):
        if name == "countries":
            return dict(US="USA", EG="Egypt", SA="Saudi", CN="China")
        elif name == "claims":
            return json.dumps(ClaimTypes)
        else:
            return JSONResponse("not found", status_code=404)






