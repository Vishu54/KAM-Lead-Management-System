from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schema.user import UserCreate, UserResponse, UserToken
from services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    from core.config import AUTH_CONTROLLER

    return AuthService(AUTH_CONTROLLER)


@router.post("/login", response_model=UserToken)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    """Authenticate user and return token"""
    token = await service.login(username=form_data.username, password=form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return token


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Contact created successfully"}, 400: {"description": "Invalid input"}, 422: {"description": "Validation error"}},
)
async def create_contact(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """Create a new contact"""
    return await auth_service.register(user.model_dump())
