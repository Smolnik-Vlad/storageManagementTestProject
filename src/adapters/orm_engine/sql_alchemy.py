from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.exceptions import DatabaseConnectionException


class SQLAlchemy:
    def __init__(self, db_url):
        try:
            engine = create_async_engine(db_url, echo=False, future=True)
            self.session_maker = async_sessionmaker(
                engine, expire_on_commit=False, autoflush=False
            )
        except DBAPIError:
            raise DatabaseConnectionException

