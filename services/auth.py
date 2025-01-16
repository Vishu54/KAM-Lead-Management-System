from fastapi import HTTPException, status
from security.auth_controller import AuthController


class AuthService:
    def __init__(self, auth_controller: AuthController) -> None:
        self.auth_controller = auth_controller
        self.user_repository = auth_controller.authn_strategy.user_repository

    async def login(self, username: str, password: str) -> dict:
        user = await self.auth_controller.authenticate(username=username, password=password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        return self.auth_controller.create_token(user)

    def register(self, user_data: dict) -> dict:
        hashed_password = self.auth_controller.authn_strategy.hash_password(user_data["password"])
        user_data["password"] = hashed_password
        return self.user_repository.create(**user_data)
