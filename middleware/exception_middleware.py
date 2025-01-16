import logging

from fastapi import HTTPException, Response, status
from fastapi.exception_handlers import http_exception_handler

from core.custom_exception import AppRuntimeException
from security.auth_controller import AuthController
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.exception_handler = http_exception_handler

    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            return await self.exception_handler(
                request, HTTPException(status_code=e.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail or "Internal server error")
            )

        except AppRuntimeException as e:
            return await self.exception_handler(request, HTTPException(status_code=e.error_code, detail=e.message))
