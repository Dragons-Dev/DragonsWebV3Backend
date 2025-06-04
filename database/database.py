from datetime import datetime

from sqlalchemy import Row, select, URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import *


class DataBase:
    """
    DataBase class handles the asynchronous database operations using SQLAlchemy.
    """

    def __init__(self, DATABASE_URL: str | URL, echo: bool = False):
        """
        Initializes the DataBase instance with an async engine and session maker.
        """
        self.logger = None  # type: ignore
        self.engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=echo)
        self.AsyncSessionLocal: AsyncSession = async_sessionmaker(self.engine, expire_on_commit=False)  # type: ignore

    async def setup(self, boot: datetime):
        """
        Sets up the database by creating new tables if they don't already exist.

        Args:
            boot (datetime): The boot time of the application.
        """
        from utils.logger import CustomLogger  # Import here to avoid circular import issues
        self.logger = CustomLogger("database", boot)  # type: ignore
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            self.logger.info("ContentDB tables created and ready to use!")

    async def insert_cookie(self, cookie: DBCookie):
        """
        Inserts a new cookie into the database.

        Args:
            cookie (DBCookie): The cookie object to be inserted.
        """
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                session.add(cookie)
                await session.commit()
                self.logger.info(f"Inserted cookie: {cookie}")

    async def update_cookie(self, cookie: DBCookie):
        """
        Updates an existing cookie in the database.

        Args:
            cookie (DBCookie): The cookie object to be updated.
        """
        async with self.AsyncSessionLocal() as session:
            await session.merge(cookie)
            await session.commit()
            self.logger.info(f"Updated cookie: {cookie}")

    async def get_cookie(self, name: str) -> DBCookie | None:
        """
        Retrieves a cookie by its name from the database.

        Args:
            name (str): The name of the cookie to retrieve.

        Returns:
            Row | None: The cookie row if found, otherwise None.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(DBCookie).where(DBCookie.name == name))
            cookie = result.scalar_one_or_none()
            if cookie:
                self.logger.info(f"Retrieved cookie: {cookie}")
            else:
                self.logger.warning(f"Cookie with name '{name}' not found.")
            return cookie

    async def delete_cookie(self, name: str) -> None:
        """
        Deletes a cookie by its name from the database.

        Args:
            name (str): The name of the cookie to delete.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(DBCookie).where(DBCookie.name == name))
            cookie = result.scalar_one_or_none()
            if cookie:
                await session.delete(cookie)
                await session.commit()
                self.logger.info(f"Deleted cookie: {cookie}")
            else:
                self.logger.warning(f"Cookie with name '{name}' not found for deletion.")
