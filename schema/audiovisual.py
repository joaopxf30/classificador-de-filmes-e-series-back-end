import regex as re
from pydantic import (
    BaseModel, 
    HttpUrl, 
    ConfigDict, 
    AliasGenerator,
    field_validator,
)
from pydantic.alias_generators import to_camel, to_pascal, to_snake
from datetime import date, time


class POSTAudiovisual(BaseModel):
    """It represents the form of a POST request for an Audiovisual's instance
    through OMDb API   

    """
    imdb_id: str | None = None
    title: str | None = None
    year: int | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
    )

    @field_validator("title")
    @classmethod
    def _replace_whitespaces_for_request(cls, v: str | None) -> str:
        return re.sub(r"\s", "+", v)


class Rating(BaseModel):
    source: str
    value: str


class Audiovisual(BaseModel):
    """It represents the response of a successful request to the OMDb Api  

    """
    title: str
    year: int
    rated: str
    released: date
    runtime: time
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    language: str
    country: str
    awards: str
    poster: HttpUrl
    ratings: list[Rating]
    metascore: int
    imdb_rating: float
    imdb_votes: float
    imdb_id: str
    type: str
    dvd: str 
    box_office: float
    production: str
    website: str
    response: bool

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
    )
    