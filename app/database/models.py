from sqlalchemy import BigInteger, Integer, String, ARRAY, PickleType
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker,create_async_engine

from ..config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(bind=engine)

class Base(AsyncAttrs,DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    cls:Mapped[str]
    name:Mapped[str]
    remaining_questions = mapped_column(PickleType) 
    answered_questions = mapped_column(PickleType, default={})



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)