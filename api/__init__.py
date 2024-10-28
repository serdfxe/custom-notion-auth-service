from fastapi import APIRouter

from api.user import user_router
from api.auth import auth_router


router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
