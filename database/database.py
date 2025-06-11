from datetime import datetime
from pathlib import Path
from os import mkdir

from sqlalchemy import Row, select, URL, or_, and_
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
        if DATABASE_URL is str:
            DATABASE_URL = URL.create(DATABASE_URL)
        if DATABASE_URL.startswith("sqlite+aiosqlite://"):
            # Ensure the directory exists for SQLite database
            path = DATABASE_URL[20:][:-12]
            db_path = Path(path)
            if db_path.exists():
                pass
            else:
                mkdir(path)
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

    async def close(self):
        await self.engine.dispose()
        await self.AsyncSessionLocal.close()

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
                self.logger.debug(f"Inserted cookie: {cookie}")

    async def update_cookie(self, cookie: DBCookie):
        """
        Updates an existing cookie in the database.

        Args:
            cookie (DBCookie): The cookie object to be updated.
        """
        async with self.AsyncSessionLocal() as session:
            await session.merge(cookie)
            await session.commit()
            self.logger.debug(f"Updated cookie: {cookie}")

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
                self.logger.debug(f"Retrieved cookie: {cookie}")
            else:
                self.logger.debug(f"Cookie with name '{name}' not found.")
            return cookie

    async def delete_cookie(self, name: str, value: str) -> None:
        """
        Deletes a cookie by its name from the database.

        Args:
            name (str): The name of the cookie to delete.
            value (str): The value of the cookie to delete.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(DBCookie).where(and_(DBCookie.name == name, DBCookie.value == value)))
            cookie = result.scalar_one_or_none()
            if cookie:
                await session.delete(cookie)
                await session.commit()
                self.logger.debug(f"Deleted cookie: {cookie}")
            else:
                self.logger.debug(f"Cookie with name '{name}' not found for deletion.")

    async def insert_authentication(self, auth: Authentication) -> None:
        """
        Creates a new authentication record in the database.

        Args:
            auth (Authentication): The authentication object to be created.
        """
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                session.add(auth)
                await session.commit()
                self.logger.debug(f"Created authentication record: {auth}")

    async def get_authentication(self, name: str) -> Authentication | None:
        """
        Retrieves an authentication record by its name from the database.

        Args:
            name (str): The name or email of the authentication record to retrieve.

        Returns:
            Authentication | None: The authentication record if found, otherwise None.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(Authentication).where(
                or_(Authentication.name == name, Authentication.mail == name)
            ))
            auth = result.scalar_one_or_none()
            if auth:
                self.logger.debug(f"Retrieved authentication record: {auth}")
            else:
                self.logger.debug(f"Authentication record with name '{name}' not found.")
            return auth

    async def update_authentication(self, name: str, auth: Authentication) -> None:
        """
        Edits an existing authentication record in the database.

        Args:
            name (str): The name or email of the authentication record to edit.
            auth (Authentication): The updated authentication object.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(Authentication).where(
                or_(Authentication.name == name, Authentication.mail == name)
            ))
            existing_auth = result.scalar_one_or_none()
            if existing_auth:
                existing_auth.name = auth.name
                existing_auth.mail = auth.mail
                existing_auth.salt = auth.salt
                existing_auth.password = auth.password
                await session.commit()
                self.logger.debug(f"Edited authentication record: {existing_auth}")
            else:
                self.logger.debug(f"Authentication record with name '{name}' not found for editing.")

    async def delete_authentication(self, name: str) -> None:
        """
        Deletes an authentication record by its name from the database.

        Args:
            name (str): The name or email of the authentication record to delete.
        """
        async with self.AsyncSessionLocal() as session:
            result = await session.execute(select(Authentication).where(
                or_(Authentication.name == name, Authentication.mail == name)
            ))
            auth = result.scalar_one_or_none()
            if auth:
                await session.delete(auth)
                await session.commit()
                self.logger.debug(f"Deleted authentication record: {auth}")
            else:
                self.logger.debug(f"Authentication record with name '{name}' not found for deletion.")
