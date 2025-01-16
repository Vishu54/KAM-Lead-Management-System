from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List

from fastapi.security import OAuth2PasswordBearer

from security.auth_controller import AuthController
from services.user import UserService
from repository.user import UserRepository
from schema.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from passlib.context import CryptContext


router = APIRouter(prefix="/user", tags=["contacts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_user_service() -> UserService:
    repository = UserRepository()
    return UserService(repository)


@router.get("/{user_id}", response_model=UserResponse, responses={200: {"description": "Contact found"}, 404: {"description": "Contact not found"}})
async def get_contact(user_id: str, service: UserService = Depends(get_user_service), token: str = Depends(oauth2_scheme)):
    """Get a contact by ID"""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return user


@router.get("/", response_model=UserListResponse, responses={200: {"description": "List of contacts retrieved successfully"}})
async def list_contacts(service: UserService = Depends(get_user_service), token: str = Depends(oauth2_scheme)):
    """Get all contacts"""
    users = await service.get_all_users()
    return UserListResponse(total=len(users), users=users)


@router.get("/restaurants/{restaurant_id}/pocs", response_model=UserListResponse, responses={200: {"description": "List of contacts retrieved successfully"}})
async def list_contacts_by_restaurant(restaurant_id: str, service: UserService = Depends(get_user_service), token: str = Depends(oauth2_scheme)):
    """Get all contacts by restaurant"""
    users = await service.get_users_by_restaurant(restaurant_id)
    return UserListResponse(total=len(users), contacts=users)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={200: {"description": "Contact updated successfully"}, 404: {"description": "Contact not found"}, 422: {"description": "Validation error"}},
)
async def update_contact(user_id: str, user_update: UserUpdate, service: UserService = Depends(get_user_service), token: str = Depends(oauth2_scheme)):
    """Update a contact"""
    updated_user = await service.update_user(user_id, user_update.model_dump(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={204: {"description": "Contact deleted successfully"}, 404: {"description": "Contact not found"}})
async def delete_contact(user_id: str, service: UserService = Depends(get_user_service), token: str = Depends(oauth2_scheme)):
    """Delete a contact"""
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Contact deleted successfully"})
