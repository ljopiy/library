from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY, ALGORITHM
from core.logging import logger
from db.session import get_session
from models import User, UserRoles
from services.user_service.user_service import get_user_by_id

o_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


DBSession = Annotated[AsyncSession, Depends(get_session)]
Token = Annotated[str, Depends(o_scheme)]


async def get_current_user(token: Token, session: DBSession) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded JWT payload: {payload}")
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db=session, user_id=user_id)
    if user is None:
        raise credentials_exception

    return user


def require_role(required_roles):
    if not isinstance(required_roles, (list, tuple, set)):
        required_roles = [required_roles]

    async def checker_role(current_user: User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Требуются роли: {', '.join([r.value for r in required_roles])}"
            )
        return current_user

    return checker_role


CurrentUser = Annotated[User, Depends(get_current_user)]

AdminUser = Annotated[User, Depends(require_role([UserRoles.ADMIN]))]

LibrarianUser = Annotated[User, Depends(require_role([UserRoles.LIBRARIAN, UserRoles.ADMIN]))]
