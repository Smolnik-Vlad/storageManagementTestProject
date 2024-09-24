from typing import AsyncGenerator

from fastapi import Depends

from src.adapters.orm_engine.sql_alchemy import SQLAlchemy
from src.core.settings import settings


class SQLAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(self) -> SQLAlchemy:
        if self.sqlalchemy is None:
            self.sqlalchemy = SQLAlchemy(settings.DATABASE_URL)
        return self.sqlalchemy


get_sql_alchemy = SQLAlchemyDependency()


async def get_db(sqlalchemy: SQLAlchemy = Depends(get_sql_alchemy)) -> AsyncGenerator:
    async with sqlalchemy.session_maker() as session:
        async with session.begin():
            yield session
