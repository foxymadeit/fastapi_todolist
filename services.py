from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import UsersModel
from security import pwd_context

# General exception for email and password
credentials_exception = HTTPException(
    status_code=401,
    detail="Incorrect email or password",
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