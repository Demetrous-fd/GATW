from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Cookie, Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from backend.security import get_jwt_strategy, get_user_manager, JWTStrategy, UserManager


def create_docs_route(app: FastAPI) -> None:
    @app.get("/docs", include_in_schema=False)
    async def get_docs(access_token: str | None = Cookie(""),
                       strategy: JWTStrategy = Depends(get_jwt_strategy),
                       user_manager: UserManager = Depends(get_user_manager)):
        user = await strategy.read_token(access_token, user_manager)
        if user is None:
            response = RedirectResponse("/login")
            response.delete_cookie("access_token")
            return response

        swagger_index = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title
        )
        swagger_index = swagger_index.body.decode("utf8")
        swagger_index = swagger_index.replace(
            "const ui = SwaggerUIBundle({\n        ",
            """const ui = SwaggerUIBundle({
                    requestInterceptor: (req) => {
                        if (req.url.includes('auth/jwt/logout')){
                            document.cookie = "access_token=0;expires='Thu, 01 Jan 1970 00:00:01 GMT'"
                            window.location.href = "/login"
                        }
                        if (! req.loadSpec) {
                            const cookie = document.cookie.split(";")
                                           .map(data => data.split("="))
                                           .reduce((accumulator, [key, value]) => 
                                               ({...accumulator, [key.trim()]: decodeURIComponent(value)}), {});
                            if (!cookie.access_token){
                                window.location.href = "/login"
                            }
                            else if (cookie.access_token && !req.headers.Authorization){
                                req.headers.Authorization = "Bearer " + cookie.access_token;
                            }
                        }
                        return req;
                    },
                            """
        )
        return HTMLResponse(swagger_index)
