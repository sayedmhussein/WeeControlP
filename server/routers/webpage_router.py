from typing import Annotated

from fastapi import Cookie
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from server.routes import PG_LOGIN, PG_INDEX


def add_webpages(app, db):
    @app.get(PG_INDEX, response_class=HTMLResponse, tags=["Webpage"])
    def index(request: Request, token: Annotated[str | None, Cookie()] = None):
        templates = Jinja2Templates(directory="templates")
        response = templates.TemplateResponse(request=request, name="index.html", context={"token": token})
        return response

    @app.get(PG_LOGIN, tags=["Webpage"])
    def login_page():
        return "This is the login screen"