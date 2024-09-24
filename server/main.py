import asyncio
import subprocess
import webbrowser

import uvicorn
from fastapi import FastAPI # pip install "fastapi[standard]"

from infrastructure.repository import engine, get_db_session
from server.route_factory import RoutingFactory
from server.services.exceptions import add_exceptions
from server.services.middlewares import ApplicationMW


def open_browser():
    subprocess.call(["sudo", "apt", "update"])
    webbrowser.open('http://127.0.0.1:8000/docs')  # Open Browser

def get_app(db):
    app = FastAPI(title="WeeControlP", summary="Application for Companies made by Python",
                  version="0.01", terms_of_service="MIT Licence",
                  contact=dict(name="Sayed M. Hussein", email="sayed.hussein@gmx.com"))

    ApplicationMW(app, db).add_middlewares()
    add_exceptions(app)

    factory = RoutingFactory(app, db)
    factory.setup_routes()
    asyncio.run(factory.setup_routes_async())

    return app


if __name__ == '__main__':
    database = get_db_session()
    application = get_app(database)
    uvicorn.run(application, host="0.0.0.0", port=8000)

