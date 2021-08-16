from app.api import router
from app.api.error import http_error_handler
from app.core.config import settings
from app.db.utils import connect_to_mongo, close_mongo_connection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.APPLICATION_NAME,
        debug=settings.DEBUG,
        version=settings.APPLICATION_VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add necessary even handlers
    application.add_event_handler("startup", connect_to_mongo)
    application.add_event_handler("shutdown", close_mongo_connection)

    # add custom exception handlers
    application.add_exception_handler(HTTPException, http_error_handler)

    # include all api routes
    application.include_router(router, prefix=settings.API_PREFIX)

    return application


app = get_application()
