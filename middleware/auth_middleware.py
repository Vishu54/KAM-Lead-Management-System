import re
from fastapi import HTTPException, status
from typing import Pattern

from core.config import PUBLIC_ENDPOINTS
from security.auth_controller import AuthController
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_controller: AuthController):
        super().__init__(app)
        self.controller = auth_controller
        self.public_paths = PUBLIC_ENDPOINTS.get("auth_not_required", [])

    def _is_path_public(self, path: str) -> bool:
        """Check if the given path is public (doesn't require authentication)."""
        # Check exact matches and regex patterns

        for public_path in self.public_paths:
            if re.match(public_path, path):
                return True

        return False

    async def dispatch(self, request, call_next):

        # Check if the path should be excluded from authentication
        if self._is_path_public(request.url.path):
            return await call_next(request)

        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user = await self.controller.verify_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user = user
        response = await call_next(request)
        return response
