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
