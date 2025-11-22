from fastapi import APIRouter

from api.admin.user import admin_user_router
from api.librarian.user import librarian_user_router
from api.user import auth

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, tags=["Authorization"])

api_router.include_router(admin_user_router, tags=["Admin Users"])

api_router.include_router(librarian_user_router, tags=["Librarian Users"])
