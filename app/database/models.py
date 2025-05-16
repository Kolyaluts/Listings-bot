from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import LargeBinary
import base64


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Listing(Base):
    __tablename__ = 'listings'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(850))
    price: Mapped[int] = mapped_column()
    city: Mapped[str] = mapped_column(String(30))
    adres: Mapped[str] = mapped_column(String(40))

    # Storing image paths (or base64 strings) for up to 5 images
    image1: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    image2: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image3: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image4: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image5: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image6: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image7: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image8: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image9: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    image10: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    telegram_id: Mapped[int] = mapped_column(nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
