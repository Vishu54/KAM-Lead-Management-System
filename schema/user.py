import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from models.user import UserRole


class UserBase(BaseModel):
    name: str = Field(..., description="User name", min_length=1, max_length=100)
    email: EmailStr = Field(..., description="User email address")
    phone: str = Field(..., description="User phone number", min_length=10, max_length=15)
    role: UserRole = Field(default=UserRole.STAFF, description="User role in the restaurant")
    restaurant_id: str = Field(..., description="ID of the associated restaurant")


class UserCreate(UserBase):
    """Schema for creating a new User"""

    password: str = Field(..., description="User password", min_length=4, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating an existing User"""

    name: Optional[str] = Field(None, description="User name", min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(None, description="User email address")
    phone: Optional[str] = Field(None, description="User phone number", min_length=10, max_length=15)
    role: Optional[UserRole] = Field(None, description="User role in the restaurant")


class UserResponse(UserBase):
    """Schema for User response"""

    user_id: uuid.UUID = Field(..., description="Unique identifier for the User", default_factory=uuid.uuid4)
    created_at: datetime = Field(..., description="Timestamp when the User was created")
    updated_at: datetime = Field(..., description="Timestamp when the User was last updated")

    class Config:
        from_attributes = True


class UserToken(BaseModel):
    """Schema for User token response"""

    access_token: str = Field(..., description="Access token for the User")
    token_type: str = Field("bearer", description="Token type")


class UserListResponse(BaseModel):
    """Schema for list of Users response"""

    total: int = Field(..., description="Total number of Users")
    users: List[UserResponse] = Field(..., description="List of Users")


class UserInDB(UserResponse):
    """Schema for User stored in the database"""

    hashed_password: str = Field(..., description="Hashed user password")
