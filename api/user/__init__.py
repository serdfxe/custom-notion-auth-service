from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status

from core.db.repository import DatabaseRepository
from core.fastapi.dependencies import get_repository
from api.auth.generate_password import hash_password
from api.auth.generate_token import JWTService
from app.models.user import User

from .dto import UserResponseDTO, UserCreateDTO
from api.auth.dto import TokenDTO

"""
Тут должны быть прописанны эндпоинты и исключения
"""

jwt_service = JWTService()

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
    422: {"description": "Bad request. Invalid input data."},
    409: {"description": "Conflict. User already exists."}
})
async def create_user_route(data: UserCreateDTO, repository: UserRepository):
    """
    Create user. The operation creates new user with provided data.
    """

    if len(await repository.filter(User.email == data.email)) > 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "error_massage": "Такая почта уже существует",
            "error_code": 1
        })
    if len(await repository.filter(User.username == data.username)) > 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "error_massage": "Такое имя уже существует",
            "error_code": 2
        })
    
    user = await repository.create({
        "username": data.username,
        "email": data.email,
        "password_hash": hash_password(data.password),
    })


    return UserResponseDTO.model_validate(user)


@user_router.delete("/", responses={
    200: {"description": "User deleted successfully."},
    401: {"description": "Unauthorized. Invalid or missing JWT token."},
    404: {"description": "User not found."}
})
async def delete_user_route(
    request: TokenDTO,
    user_repo: UserRepository,
    ):
    """
    Delete user. The operation deletes user that is associated with the provided JWT token.
    """
    try:
        payload = jwt_service.decode_jwt(request.token)
    except Exception:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user_id = payload.get('sub')

    if user_id is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain user ID",
        )

    user = await user_repo.get(user_id)

    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    await user_repo.delete(user_id)

    return {"detail": "User deleted successfully"}




