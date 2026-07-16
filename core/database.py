from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator


#Notice the driver specification: sqlite+aiosqlite
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

#connect_args = {"check_same_thread": False} is required ONLY for SQLite

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit =False  #prevents attributes from becoming stale/inaccessible after commit
    )


Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yields an independent asynchronous transaction session per HTTP request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            pass  #the async context manager already closes the session on exit     
    
    