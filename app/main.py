from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.api.error import http_error_handler
from fastapi.middleware.cors import CORSMiddleware
from app.db.utils import connect_to_mongo, close_mongo_connection


from app.api import router


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
    application.add_event_handler("startup", connect_to_mongo)
    application.add_event_handler("shutdown", close_mongo_connection)

    application.add_exception_handler(HTTPException, http_error_handler)

    application.include_router(router, prefix=settings.API_PREFIX)

    return application


app = get_application()
