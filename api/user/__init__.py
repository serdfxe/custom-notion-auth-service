from typing import Annotated

from fastapi import APIRouter, Request, Depends

from core.db.repository import DatabaseRepository
from core.fastapi.dependencies import get_repository

from app.models.user import User

from .dto import UserResponseDTO, UserCreateDTO


UserRepository = Annotated[
    DatabaseRepository[User],
    Depends(get_repository(User)),
]

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/", response_model=UserResponseDTO, responses={
    200: {"description": "User data retrieved successfully."},
    401: {"description": "Unauthorized. Invalid or missing JWT token."},
    404: {"description": "User not found."}
})
async def get_user_route(request: Request):
    """
    Get user data. The operation returns the data of the user that is associated with the provided JWT token.
    """
    
@user_router.post("/", response_model=UserResponseDTO, responses={
    201: {"description": "User created successfully."},
    400: {"description": "Bad request. Invalid input data."},
    409: {"description": "Conflict. User already exists."}
})
async def create_user_route(data: UserCreateDTO, repository: UserRepository):
    """
    Create user. The operation creates new user with provided data.
    """
    user = await repository.create(data.dict())
    
    return UserResponseDTO.from_orm(user)
    
@user_router.delete("/", responses={
    200: {"description": "User deleted successfully."},
    401: {"description": "Unauthorized. Invalid or missing JWT token."},
    404: {"description": "User not found."}
})
async def delete_user_route(request: Request):
    """
    Delete user. The operation deletes user that is associated with the provided JWT token.
    """
