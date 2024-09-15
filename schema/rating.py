from pydantic import BaseModel, ConfigDict
from constants import Notes
from uuid import UUID


class PostRating(BaseModel):
    """It represents the form of a POST request in order to give
    a rating for some movie or series.

    """
    audiovisual_id: UUID
    rating: Notes


class PutRating(BaseModel):
    """It represents the form of a PUT request in order to change
    the rating for some movie or series.

    """
    audiovisual_id: UUID
    rating: Notes

    
class RatingView(BaseModel):
    """It represents how an instance of Rating is returned.

    """
    rating: Notes

    model_config = ConfigDict(
        from_attributes=True,
    )


class RatingQuery(BaseModel):
    """It represents the parameters for a query to a rating's movie 
    or series.

    """
    audiovisual_id: str
