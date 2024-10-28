from fastapi import APIRouter, Request, Response

from .dto import TokenResponseDTO, TokenRequestDTO

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/token", response_model=TokenResponseDTO, responses={
    200: {"description": "Token generated successfully."},
    403: {"description": "Forbidden. Invalid credentials."},
    500: {"description": "Server error. Unable to generate token."}
})
def get_token_route(request: TokenRequestDTO):
    """
    Get token. The operation returns JWT token.
    """

@auth_router.get("/verify", responses={
    200: {"description": "Token is valid."},
    401: {"description": "Invalid token."},
    500: {"description": "Server error during verification."}
})
def verify_token_route(request: Request, response: Response):
    """
    Verify token. The operation verifies provided JWT token and send user id in response in header x-user-id.
    """
