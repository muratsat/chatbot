from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VectorStore(Base):
    __tablename__ = "vector_stores"

    id: Mapped[str] = mapped_column(primary_key=True)
