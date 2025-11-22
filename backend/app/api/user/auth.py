from fastapi import APIRouter
from fastapi import Form, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from core.security import create_access_token
from db.session import get_session
from models import UserRoles
from schemas.token import Token
from schemas.user import UserRegisterResponse
from services.user_service.user_service import authenticate_user_by_ticket, create_user

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserRegisterResponse)
async def register_user_form(
        role: UserRoles = Form(...),
        db: AsyncSession = Depends(get_session),
):
    user, raw_password = await create_user(db, role=role)

    return UserRegisterResponse(
        id=user.id,
        ticket_id=user.ticket_id,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        password=raw_password,
    )


@router.post("/login", response_model=Token)
async def login_form(
        username: str = Form(...),
        password: str = Form(...),
        db: AsyncSession = Depends(get_session),
):
    try:
        user = await authenticate_user_by_ticket(db, username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            user_id=user.id,
            ticket_id=user.ticket_id,
            role=user.role.value,
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error during login for %s: %s", username, e)
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        logger.exception("Unexpected error during login for %s", username)
        raise HTTPException(status_code=500, detail="Unexpected error")
