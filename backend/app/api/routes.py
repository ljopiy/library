from fastapi import APIRouter

from api.admin.librarian import admin_librarian_router
from api.admin.user import admin_user_router
from api.librarian.book import librarian_books_router
from api.librarian.genre import librarian_genres_series_router
from api.librarian.user import librarian_user_router
from api.user import auth
from api.user.user import me_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, tags=["Authorization"])
api_router.include_router(me_router, tags=["My Profile"])

api_router.include_router(admin_user_router, tags=["Admin Users"])
api_router.include_router(admin_librarian_router, tags=["Admin Librarians"])

api_router.include_router(librarian_user_router, tags=["Librarian Users"])
api_router.include_router(librarian_books_router, tags=["Librarian Books"])
api_router.include_router(librarian_genres_series_router, tags=["Genres & Series"])
