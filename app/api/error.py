from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse


def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
