from uuid import uuid4, UUID

from sqlalchemy import (
    Integer,
    Float,
    String,
    Boolean,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import ClassificadorFilmesSeriesBase


class Audiovisual(ClassificadorFilmesSeriesBase):
    __tablename__ = "audiovisual"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(50), nullable=True)
    rated: Mapped[str] = mapped_column(String(50), nullable=True)
    released: Mapped[str] = mapped_column(String(50), nullable=True)
    runtime: Mapped[str] = mapped_column(String(50), nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    director: Mapped[str] = mapped_column(String(50), nullable=True)
    writer: Mapped[str] = mapped_column(String(50), nullable=True)
    actors: Mapped[str] = mapped_column(String(50), nullable=True)
    plot: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    awards: Mapped[str] = mapped_column(String(50), nullable=True)
    poster: Mapped[str] = mapped_column(String(100), nullable=True)
    metascore: Mapped[int] = mapped_column(Integer, nullable=True)
    imdb_rating: Mapped[float] = mapped_column(Float, nullable=True)
    imdb_votes: Mapped[float] = mapped_column(Float, nullable=True)
    imdb_id: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    dvd: Mapped[str] = mapped_column(String(50), nullable=True)
    total_seasons: Mapped[str] = mapped_column(String(50), nullable=True)
    box_office: Mapped[str] = mapped_column(String(50), nullable=True)
    production: Mapped[str] = mapped_column(String(50), nullable=True)
    website: Mapped[str] = mapped_column(String(50), nullable=True)
    response: Mapped[bool] = mapped_column(Boolean, nullable=False)
