import regex as re
import logging
from pydantic import (
    BaseModel, 
    HttpUrl, 
    ConfigDict, 
    AliasGenerator,
    AliasChoices,
    field_validator,
    Field,
)
from pydantic.alias_generators import to_camel, to_pascal, to_snake
from typing import Any

LOG = logging.getLogger()


class POSTAudiovisual(BaseModel):
    """It represents the form of a POST request for an Audiovisual's instance
    through OMDb API   

    """
    imdb_id: str | None = Field(default=None, validation_alias="IMDbID")
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
        return re.sub(r"\s", "+", v) if v else v


class Audiovisual(BaseModel):
    """It represents the response of a successful request to the OMDb Api  

    """
    title: str | None
    year: str | int | None
    rated: str | None
    released: str | None
    runtime: str | None
    genre: str | None
    director: str | None
    writer: str | None
    actors: str | None
    plot: str | None
    language: str | None
    country: str | None
    awards: str | None
    poster: str | None
    ratings: list["Rating"] | None
    metascore: int | None
    imdb_rating: float | None
    imdb_votes: float | None
    imdb_id: str | None = Field(validation_alias="imdbID")
    type: str | None
    dvd: str | None = Field(default=None, validation_alias="DVD")
    total_seasons: str | None = None
    box_office: str | None = None
    production: str | None = None
    website: str | None = None
    response: bool

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias= lambda f: AliasChoices(
                to_camel(f),
                to_pascal(f), 
            ),
            serialization_alias=to_snake,
        ),
    )
    
    @field_validator("imdb_rating", "imdb_votes", mode="before")
    @classmethod
    def _change_commma_to_dot(cls, v: float | None) -> float | None:
        if v and re.search(r",", v):
            return float(re.sub(",", ".", v))
        
        return v
    
    @field_validator("*", mode="before")
    def _empty_field(cls, v: Any) -> str | None:
        if isinstance(v, str) and re.search(r"N/A", v):
            return None
    
        return v
    

class Rating(BaseModel):
    source: str
    value: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_pascal,
            serialization_alias=to_snake,
        ),
    )