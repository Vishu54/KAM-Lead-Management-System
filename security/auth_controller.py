from typing import Optional

from fastapi import status, HTTPException, Request

from schema.user import UserInDB
from security.authentication import BaseAuthenticator, BaseTokenStrategy
from security.authorization import AuthorizationFilter


class AuthController:
    def __init__(self, auth_strategy: BaseAuthenticator, token_strategy: BaseTokenStrategy):
        self.authn_strategy = auth_strategy
        self.token_strategy = token_strategy

    async def authenticate(self, **credentials) -> Optional[UserInDB]:
        """Authenticate user with provided credentials"""
        return await self.authn_strategy.authenticate_user(**credentials)

    async def verify_token(self, token: str) -> Optional[UserInDB]:
        """Verify authentication token"""
        return self.token_strategy.verify_token(token)

    def create_token(self, user: UserInDB) -> dict:
        """Create authentication token"""
        access_token = self.token_strategy.create_token(user)
        return {"access_token": access_token, "token_type": "bearer"}

    async def authorize(self, user: UserInDB, request: Request, authz: AuthorizationFilter) -> bool:
        """Check if user is authorized"""
        return await authz.authorize(user, request)

    def requires(self, role_filter: AuthorizationFilter):
        async def authorization_dependency(request: Request) -> None:
            user = await self.authn_strategy.user_repository.get_by_email(email=request.state.user.get("sub"))
            if not await self.authorize(user, request, role_filter):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        return authorization_dependency
