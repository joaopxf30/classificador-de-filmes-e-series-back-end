from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake
from uuid import UUID


class PostRating(BaseModel):
    """It represents the form of a POST request in order to create
    a tuple for a movie or series in the rating's table.

    """
    audiovisual_id: UUID
    rating: float | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
    )


class PutRating(BaseModel):
    """It represents the form of a PUT request in order to change
    the rating for some movie or series.

    """
    audiovisual_id: UUID
    rating: float

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
    )
    

class RatingView(BaseModel):
    """It represents how an instance of Rating is returned.

    """
    rating: float | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class RatingQuery(BaseModel):
    """It represents the parameters for a query to a rating's movie 
    or series.

    """
    audiovisual_id: str
