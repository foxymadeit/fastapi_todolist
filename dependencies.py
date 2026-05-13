from fastapi import Depends
from fastapi import Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from services import get_current_user
from models import UsersModel
from schemas import PaginationSchema, SortEnum
from security import http_bearer

def pagination_params(
        page: int = Query(ge=1,default=1),
        limit: int = Query(ge=1, le=100, default=10),
        order: SortEnum = SortEnum.DESC
):
    return PaginationSchema(page=page, limit=limit, order=order)


TokenDep = Annotated[str, Depends(http_bearer)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
UserDep = Annotated[UsersModel, Depends(get_current_user)]
PaginationDep = Annotated[PaginationSchema, Depends(pagination_params)]