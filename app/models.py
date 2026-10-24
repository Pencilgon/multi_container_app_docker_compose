from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class MediaEntry(Base):
    __tablename__ = "media_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200))

    media_type: Mapped[str] = mapped_column(String(30))

    release_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    recovery_status: Mapped[str] = mapped_column(
        String(30),
        default="lost",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )