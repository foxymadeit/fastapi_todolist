from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import select
from models import UsersModel
from security import pwd_context
from database import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
http_bearer = HTTPBearer()

# Dependencies
TokenDep = Annotated[str, Depends(http_bearer)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]

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


async def get_current_user(session: SessionDep,
                    token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = await session.get(UsersModel, int(user_id))
        if user_id is None:
         raise credentials_exception
        return user
    except InvalidTokenError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception



UserDep = Annotated[UsersModel, Depends(get_current_user)]
