from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from fastapi.security import OAuth2PasswordBearer

from services.order import OrderService
from services.interaction import InteractionService
from repository.order import OrderRepository
from repository.interaction import InteractionRepository
from schema.order import OrderCreate, OrderResponse, OrderListResponse
from models.order import OrderStatus

router = APIRouter(prefix="/orders", tags=["orders"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_order_service() -> OrderService:
    repository = OrderRepository()
    interaction_service = InteractionService(InteractionRepository())
    return OrderService(repository, interaction_service)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Order created successfully"}, 400: {"description": "Invalid order data"}, 500: {"description": "Internal server error"}},
)
async def place_order(order: OrderCreate, service: OrderService = Depends(get_order_service), token: str = Depends(oauth2_scheme)):
    """Place a new order"""
    return await service.place_order(order.model_dump())


@router.get(
    "/restaurants/{restaurant_id}",
    response_model=OrderListResponse,
    responses={200: {"description": "List of orders retrieved successfully"}, 500: {"description": "Internal server error"}},
)
async def list_restaurant_orders(restaurant_id: str, service: OrderService = Depends(get_order_service), token: str = Depends(oauth2_scheme)):
    """Get all orders for a restaurant"""
    orders = await service.get_restaurant_orders(restaurant_id)
    return OrderListResponse(total=len(orders), orders=orders)


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    responses={200: {"description": "Order status updated successfully"}, 404: {"description": "Order not found"}, 500: {"description": "Internal server error"}},
)
async def update_order_status(order_id: str, status: OrderStatus, service: OrderService = Depends(get_order_service), token: str = Depends(oauth2_scheme)):
    """Update the status of an order"""
    return await service.update_order_status(order_id, status)
