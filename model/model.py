from uuid import uuid4, UUID

from sqlalchemy import Integer, Float, String, Boolean, UUID as uuid, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import MoviesAndSeriesBase


class Audiovisual(MoviesAndSeriesBase):
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
    imdb_votes: Mapped[str] = mapped_column(String(50), nullable=True)
    imdb_id: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    dvd: Mapped[str] = mapped_column(String(50), nullable=True)
    total_seasons: Mapped[str] = mapped_column(String(50), nullable=True)
    box_office: Mapped[str] = mapped_column(String(50), nullable=True)
    production: Mapped[str] = mapped_column(String(50), nullable=True)
    website: Mapped[str] = mapped_column(String(50), nullable=True)
    response: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rating: Mapped["Rating"] = relationship(
        back_populates="audiovisual",
        cascade="all, delete",
    )


class Rating(MoviesAndSeriesBase):
    __tablename__ = "rating"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    audiovisual_id: Mapped[UUID] = mapped_column(
        ForeignKey("audiovisual.id", ondelete="CASCADE"), unique=True
    )
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    audiovisual: Mapped["Audiovisual"] = relationship(back_populates="rating")
