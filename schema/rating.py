from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake
from uuid import UUID


class RatingPost(BaseModel):
    """It represents the form of a POST request in order to give
    the first rating for a movie or series in the rating's table.

    """

    audiovisual_id: UUID
    rating: float

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
        json_schema_extra={
            "example": {
                "audiovisualId": "01f538ec-4c9b-4019-925a-2badaef4d784",
                "rating": 3.5,
            }
        },
    )


class RatingPut(BaseModel):
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
        json_schema_extra={
            "example": {
                "audiovisualId": "01f538ec-4c9b-4019-925a-2badaef4d784",
                "rating": 2.0,
            }
        },
    )


class RatingView(BaseModel):
    """It represents how an instance of Rating is returned."""

    rating: float | None

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": {"rating": 2.0}}
    )


class RatingQuery(BaseModel):
    """It represents the parameters for a query to a rating's movie
    or series.

    """

    audiovisual_id: str

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_snake,
        ),
        json_schema_extra={
            "example": {"audiovisualId": "01f538ec-4c9b-4019-925a-2badaef4d784"}
        },
    )


class RatingRemovedMessage(BaseModel):
    """It represents when a rating is removed."""

    message: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "Previous rating has been removed"}}
    )


class RatingErrorMessage(BaseModel):
    """It represents a not sucessful request"""

    message: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "This is an error message"}}
    )
