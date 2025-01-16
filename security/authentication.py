from abc import ABC, abstractmethod
from typing import Optional
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt

from repository.user import UserRepository


class BaseAuthenticator(ABC):
    def __init__(self) -> None:
        self.user_repository: UserRepository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_user(self, username: str) -> Optional[dict]:
        pass


class BaseTokenStrategy(ABC):
    @abstractmethod
    def create_token(self, user: dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[dict]:
        pass


class JWTTokenStrategy(BaseTokenStrategy):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, user: dict) -> str:
        data = {"sub": user.email}
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Could not validate credentials")


class DatabaseAuthenticator(BaseAuthenticator):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        super().__init__()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user = await self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_user(self, username: str) -> Optional[dict]:
        user = await self.user_repository.get_by_email(username)
        return user
