from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import AUTH_CONTROLLER
from core.database import get_db
from repository.restaurant import RestaurantRepository
from security.auth_controller import AuthController
from security.authorization import RoleFilter
from services.restaurant import RestaurantService
from schema.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantListResponse


router = APIRouter(prefix="/restaurants", tags=["restaurants"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_restaurant_service() -> RestaurantService:
    repository = RestaurantRepository()
    return RestaurantService(repository)


@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Restaurant created successfully"}, 400: {"description": "Invalid input"}, 422: {"description": "Validation error"}},
)
async def create_restaurant(restaurant: RestaurantCreate, service: RestaurantService = Depends(get_restaurant_service), token: str = Depends(oauth2_scheme)):
    """Create a new restaurant"""
    return await service.create_restaurant(restaurant.model_dump())


@router.get("/{restaurant_id}", response_model=RestaurantResponse, responses={200: {"description": "Restaurant found"}, 404: {"description": "Restaurant not found"}})
async def get_restaurant(restaurant_id: str, service: RestaurantService = Depends(get_restaurant_service), token: str = Depends(oauth2_scheme)):
    """Get a restaurant by ID"""
    restaurant = await service.get_restaurant_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return restaurant


@router.get("/", response_model=RestaurantListResponse, responses={200: {"description": "List of restaurants retrieved successfully"}})
async def list_restaurants(
    service: RestaurantService = Depends(get_restaurant_service),
    _: None = Depends(AUTH_CONTROLLER.requires(RoleFilter(["Staff", "Admin"], True))),
    token: str = Depends(oauth2_scheme),
):
    """Get all restaurants"""
    restaurants = await service.get_all_restaurants()
    return RestaurantListResponse(total=len(restaurants), restaurants=restaurants)


@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    responses={200: {"description": "Restaurant updated successfully"}, 404: {"description": "Restaurant not found"}, 422: {"description": "Validation error"}},
)
async def update_restaurant(
    restaurant_id: str, restaurant_update: RestaurantUpdate, service: RestaurantService = Depends(get_restaurant_service), token: str = Depends(oauth2_scheme)
):
    """Update a restaurant"""
    updated_restaurant = await service.update_restaurant(restaurant_id, restaurant_update.model_dump(exclude_unset=True))
    if not updated_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return updated_restaurant


@router.patch(
    "/{restaurant_id}/status",
    response_model=RestaurantResponse,
    responses={200: {"description": "Restaurant status updated successfully"}, 404: {"description": "Restaurant not found"}},
)
async def update_restaurant_status(restaurant_id: str, status: str, service: RestaurantService = Depends(get_restaurant_service), token: str = Depends(oauth2_scheme)):
    """Update a restaurant status"""
    updated_restaurant = await service.update_restaurant_status(restaurant_id, status)
    if not updated_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return updated_restaurant


@router.delete(
    "/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT, responses={204: {"description": "Restaurant deleted successfully"}, 404: {"description": "Restaurant not found"}}
)
async def delete_restaurant(restaurant_id: str, service: RestaurantService = Depends(get_restaurant_service), token: str = Depends(oauth2_scheme)):
    """Delete a restaurant"""
    deleted = await service.delete_restaurant(restaurant_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Restaurant deleted successfully"})
