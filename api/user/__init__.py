from fastapi import APIRouter, Request

from .dto import UserResponseDTO, UserCreateDTO


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/", response_model=UserResponseDTO, responses={
    200: {"description": "User data retrieved successfully."},
    401: {"description": "Unauthorized. Invalid or missing JWT token."},
    404: {"description": "User not found."}
})
def get_user_route(request: Request):
    """
    Get user data. The operation returns the data of the user that is associated with the provided JWT token.
    """
    
@user_router.post("/", response_model=UserResponseDTO, responses={
    201: {"description": "User created successfully."},
    400: {"description": "Bad request. Invalid input data."},
    409: {"description": "Conflict. User already exists."}
})
def create_user_route(request: UserCreateDTO):
    """
    Create user. The operation creates new user with provided data.
    """
    
@user_router.delete("/", responses={
    200: {"description": "User deleted successfully."},
    401: {"description": "Unauthorized. Invalid or missing JWT token."},
    404: {"description": "User not found."}
})
def delete_user_route(request: Request):
    """
    Delete user. The operation deletes user that is associated with the provided JWT token.
    """
