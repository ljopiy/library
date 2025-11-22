from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from core.security import verify_password, hash_password
from models import User
from schemas.change_password import ChangePasswordRequest
from schemas.user import AdminUserUpdate


async def update_profile_service(
        update_data: AdminUserUpdate,
        current_user: User,
        db: AsyncSession,
) -> User:
    try:
        if update_data.full_name is not None:
            current_user.full_name = update_data.full_name
        if update_data.email is not None:
            current_user.email = update_data.email
        if update_data.role is not None:
            current_user.role = update_data.role
        if update_data.is_active is not None:
            current_user.is_active = update_data.is_active

        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)

        return current_user

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            "Database error while updating profile for user %s: %s",
            getattr(current_user, "id", None),
            e,
        )
        raise HTTPException(status_code=500, detail="Database error during profile update")

    except Exception as e:
        logger.exception(
            "Unexpected error while updating profile for user %s",
            getattr(current_user, "id", None),
        )
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during profile update: {type(e).__name__}",
        )


async def change_password_service(
        data: ChangePasswordRequest,
        current_user: User,
        db: AsyncSession,
) -> User:
    try:
        if not verify_password(data.old_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Старый пароль неверен")

        current_user.hashed_password = hash_password(data.new_password)

        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)

        return current_user

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(
            "Database error while changing password for user %s: %s",
            getattr(current_user, "id", None),
            e,
        )
        raise HTTPException(status_code=500, detail="Database error during password change")

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            "Unexpected error while changing password for user %s",
            getattr(current_user, "id", None),
        )
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during password change: {type(e).__name__}",
        )
