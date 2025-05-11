import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from backend.api.auth import auth_router
from backend.api.companies import companies_router
from backend.api.news import news_router
from backend.dependencies import get_user
from fastapi.middleware.cors import CORSMiddleware
from backend.models.base.users import User
from backend.settings import get_app_settings
from backend.utils.api_helpers import register_routers
from backend.utils.exceptions import ServiceException, exception_handler
from backend.utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

LOG = get_logger()
app_settings = get_app_settings()

app = FastAPI(
    title="Virtual Insights Backend APIs",
    version="2.0.0",
    description="APIs for Virtual Insights Backend",
    docs_url="/swagger",
)

routers = [companies_router, news_router]

unprotected_routers = [auth_router]

if app_settings.local:
    LOG.info(
        f"Running in local mode. Hence all routes are unprotected. This is for local development. Please use the mock user ({app_settings.local_user_email}) for authentication."
    )
    """
    In local mode, we don't need to authenticate the routes
    """

    def get_user_override():
        return User(
            user_id=app_settings.local_user_email,
        )

    app.dependency_overrides[get_user] = get_user_override

_unprotected_routes = register_routers(
    app, protected_routers=routers, unprotected_routers=unprotected_routers
)

# app.add_middleware(middleware_class=get_auth_middleware(app, _unprotected_routes+["/docs"]))
app.add_exception_handler(ServiceException, exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5173"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=True)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
