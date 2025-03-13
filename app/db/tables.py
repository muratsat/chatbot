from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VectorStore(Base):
    __tablename__ = "vector_stores"

    id: Mapped[str] = mapped_column(primary_key=True)


class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(primary_key=True)
    vector_store_id: Mapped[str] = mapped_column(ForeignKey("vector_stores.id"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now())
    response_id: Mapped[str] = mapped_column(nullable=True)
