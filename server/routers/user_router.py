from typing import Union

from markupsafe import escape
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from server.routers.base_router import BaseContext
from server.routes import PG_USER, PG_LOGIN, V2_USER, V2_USER_AUTHENTICATION
from server.services.authorization import authorize
from application.contexts.user_service import UserService


# Login Data Transfer Object Comment by Sayed
class LoginDto(BaseModel):
    username: str
    password: str

# New User DTO
class UserDto(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    mobile: str | None = None

class UserContext(BaseContext):
    def __init__(self, app, db):
        super().__init__(app, db)
        self.service = UserService(db)

    def setup_routing(self):
        @self.app.get(PG_USER, tags=["Webpage"])
        def user_main_page():
            return "This is user main page"

        @self.app.post(V2_USER, tags=["Webpage"])
        def login(dto: LoginDto):
            # Create cookie which contains the user details.
            return "do_the_login()"

        @self.app.get(PG_LOGIN, tags=["Webpage"])
        def login_page():
            return "This is the login screen"

    async def setup_routing_async(self):
        @self.app.get(PG_USER + "{username}", tags=["User"])
        async def show_user_profile(username):
            # show the user profile for that user
            return f'User {escape(username)}'

        @self.app.post(PG_USER, tags=["User"])
        async def user_main_page(dto: UserDto):
            return "success"

        @self.app.put(PG_USER + "{username}", tags=["User"])
        async def show_user_profile(username, p: Union[str, None] = None, v: Union[str, None] = None):
            # edit user data
            return f'User {escape(username)}'

        @self.app.delete(PG_USER, tags=["User"])
        async def delete_user():
            return "User Delete Function"

        @self.app.post(V2_USER_AUTHENTICATION, tags=["Authentication"])
        def user_login(dto: LoginDto, request: Request):
            # create new session and return token using credentials.
            token = self.service.create_token(dto.username, dto.password, request.state.device)
            response = JSONResponse(dict(token=token))
            response.set_cookie("token", token)
            return response

        @self.app.head(V2_USER_AUTHENTICATION, tags=["Authentication"])
        @authorize()
        async def user_token(request: Request):
            # refresh existing user token using old token, user must be legislate.
            token = await self.service.update_token(request.state.session, request.state.device)
            response = JSONResponse(dict(token=token))
            response.set_cookie("token", token)
            return response


        @self.app.delete(V2_USER_AUTHENTICATION, tags=["Authentication"])
        @authorize()
        async def user_logout(request: Request):
            # close the user session using existing token
            await self.service.terminate_token(request.state.session, request.state.device)
            response = JSONResponse(dict(response="Good by :)"))
            response.delete_cookie("token")
            return response
