from fastapi import HTTPException
from fastapi import Depends
from database import get_session
from security import http_bearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import UsersModel
from security import pwd_context
import jwt
from jwt.exceptions import InvalidTokenError
from config import settings

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.ALGORITHM



# General exception for email and password
credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Function to find user's email in database
async def get_user_by_email(email: str, session: AsyncSession):
    query = select(UsersModel).where(UsersModel.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


# Function to match user's password with hashed password in database
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
         raise credentials_exception
        user = await session.get(UsersModel, int(user_id))
        return user
    except InvalidTokenError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception


def log_task_created(task_title: str, user_id: int):
    print(f"[LOG] User: {user_id} created task: '{task_title}'")
