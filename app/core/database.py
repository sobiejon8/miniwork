from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# SQLAlchemy modellari uchun asosiy baza klassi
class Base(DeclarativeBase):
    pass


# Asinxron ma'lumotlar bazasi dvigatelini (engine) yaratish
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Sessiyalar fabrikasi
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# FastAPI endpointlari uchun baza sessiyasi
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
