from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from services.interaction import InteractionService
from repository.interaction import InteractionRepository
from schema.interaction import InteractionCreate, InteractionResponse, InteractionListResponse


router = APIRouter(prefix="/interactions", tags=["interactions"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_interaction_service() -> InteractionService:
    repository = InteractionRepository()
    return InteractionService(repository)


@router.post(
    "/",
    response_model=InteractionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Interaction created successfully"}, 400: {"description": "Invalid input"}, 422: {"description": "Validation error"}},
)
async def create_interaction(interaction: InteractionCreate, service: InteractionService = Depends(get_interaction_service), token: str = Depends(oauth2_scheme)):
    """Create a new interaction"""
    return await service.create_interaction(interaction.model_dump())


@router.get("/{interaction_id}", response_model=InteractionResponse, responses={200: {"description": "Interaction found"}, 404: {"description": "Interaction not found"}})
async def get_interaction(interaction_id: str, service: InteractionService = Depends(get_interaction_service), token: str = Depends(oauth2_scheme)):
    """Get an interaction by ID"""
    interaction = await service.get_interaction_by_id(interaction_id)
    if not interaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interaction not found")
    return interaction


@router.get("/", response_model=InteractionListResponse, responses={200: {"description": "List of interactions retrieved successfully"}})
async def list_interactions(service: InteractionService = Depends(get_interaction_service), token: str = Depends(oauth2_scheme)):
    """Get all interactions"""
    interactions = await service.get_all_interactions()
    return InteractionListResponse(total=len(interactions), interactions=interactions)


@router.get("/restaurants/{restaurant_id}", response_model=InteractionListResponse, responses={200: {"description": "List of interactions retrieved successfully"}})
async def list_interactions_by_restaurant(restaurant_id: str, service: InteractionService = Depends(get_interaction_service), token: str = Depends(oauth2_scheme)):
    """Get all interactions by restaurant"""
    interactions = await service.get_interactions_by_restaurant(restaurant_id)
    return InteractionListResponse(total=len(interactions), interactions=interactions)


@router.get("/contacts/{user_id}", response_model=InteractionListResponse, responses={200: {"description": "List of interactions retrieved successfully"}})
async def list_interactions_by_contact(user_id: str, service: InteractionService = Depends(get_interaction_service), token: str = Depends(oauth2_scheme)):
    """Get all interactions by contact"""
    interactions = await service.get_interactions_by_contact(user_id)
    return InteractionListResponse(total=len(interactions), interactions=interactions)
