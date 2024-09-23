import logging
import pdb
from uuid import UUID

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model import Session
import model.model as model

from omdb_api import OMDbApi, DataNotFoundException

from sqlalchemy.exc import IntegrityError

from schema import (
    PostAudiovisual, 
    Audiovisual,
    AudiovisualView,
    AudiovisualQuery,
    PostRating,
    PutRating,
    RatingView,
    RatingQuery,
)

from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

LOG = logging.getLogger()


AUDIOVISUAL_TAG = Tag(
    name="Audiovisual", 
    description="Addition, view and removal of movies and series"
)
RATING_TAG = Tag(
    name="Rating",
    description="Addition, view, edit and removal of movies and series' tag"
)
HOME_TAG = Tag(
    name="Documentation", 
    description="Documentation forms: Swagger, Redoc or RapiDoc"
)


@app.get(
    "/", 
    tags=[HOME_TAG]
)
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect("/openapi")


@app.get(
    "/audiovisuals", 
    tags=[AUDIOVISUAL_TAG],
    responses={
        "200": AudiovisualView, 
        # "404": ErrorSchema,
    }
)
def get_audiovisuals():
    """Get all previous movies or series and the given rating
    from the collection. If the audiovisual has not been yet
    rated, the rating attribute is None.

    """
    LOG.info(f"Collecting movies and series")
    with Session() as session:
        if db_data := session.query(model.Audiovisual).all():
            LOG.info("There are %d movies and series on the collection" % len(db_data))
            audiovisuals_view = list(
                map(
                    lambda v: AudiovisualView.model_validate(v),
                    db_data
                )
            )
            return {"audiovisuals": [v.model_dump() for v in audiovisuals_view]}, 200
        
        return {"audiovisuals": []}, 200
        

@app.post(
    rule="/add_audiovisual", 
    tags=[AUDIOVISUAL_TAG],
    responses={
        "200": AudiovisualView,
        # "400": ErrorSchema,
        # "409": ErrorSchema,
    }
)
def add_audiovisual(form: PostAudiovisual):
    """Add a new movie or series to the collection

    """
    session = Session()

    try:
        response = OMDbApi().get_audiovisual(**form.model_dump())
    except DataNotFoundException as e:
        return {"message": e.msg}, 400

    audiovisual = Audiovisual.model_validate(response.json())
    serial = audiovisual.model_dump(exclude={"ratings"})
    db_data = model.Audiovisual(**serial)

    try:
        LOG.info(f"Trying to add the movie or series {audiovisual.title} to the collection")
        session.add(db_data)        
        session.commit()
        
        audiovisual_view = AudiovisualView.model_validate(db_data)

        return audiovisual_view.model_dump(), 200

    except IntegrityError:
        # Unique constraint disrespected
        error_msg = f"The movie or series {audiovisual.title} has been already added"
        LOG.warning(error_msg)

        return {"message": error_msg}, 409

    except Exception:
        # Dealing with general exceptions
        error_msg = (
            "It was not possible to add the movie or "
            f"series {audiovisual.title} to the collection"
        )
        LOG.warning(error_msg)

        return {"message": error_msg}, 400
    

@app.delete(
    rule="/delete_audiovisual", 
    tags=[AUDIOVISUAL_TAG],
    responses={
        # "200": EsportistaDeletadoSchema, 
        # "404": ErrorSchema
    }
)
def delete_audiovisual(query: AudiovisualQuery):
    """Delete a movie or series from the collection and
    its rating if it was rated before.

    """
    session = Session()

    if session.query(model.Audiovisual).filter(
        model.Audiovisual.id == UUID(unquote(query.id))
    ).delete():
        
        session.commit()
        msg = "Movie or series removed"
        LOG.info(f"Movie or series is no longer on the collection")
        return {"message": msg}, 200
    
    error_msg = f"There is no movie or series related to {query.id}"
    LOG.warning(f"{error_msg}")
    return {"message": error_msg}, 404


@app.post(
    rule="/add_rating", 
    tags=[RATING_TAG],
    responses={
        "200": RatingView,
        # "400": ErrorSchema,
        # "409": ErrorSchema,
    }
)
def add_rating(form: PostRating):
    """Add a rating to a movie or series from the the collection

    """
    session = Session()
    
    db_data = model.Rating(**form.model_dump())

    try:
        LOG.info(f"Trying to add rating for movie or series")
        session.add(db_data)        
        session.commit()

        rating_view = RatingView.model_validate(db_data)
        
        return rating_view.model_dump(), 200
    
    except IntegrityError as e:
        integrity_error = e.orig.sqlite_errorname

        if integrity_error == "SQLITE_CONSTRAINT_UNIQUE":
            # Constaint unique disrespected
            
            audiovisual = Session().query(model.Audiovisual).filter(
                model.Audiovisual.id == form.audiovisual_id
            ).one()

            error_msg = (
                "It is not possible to add another note for "
                f"{audiovisual.title}. A PUT request should "
                "be done instead."
            )
        
        elif integrity_error == "SQLITE_CONSTRAINT_FOREIGNKEY":
            # Foreign key constraint disrespected
            error_msg = (
                f"The uuid code {form.audiovisual_id} is not "
                "related to any movie or series from the collection"
            )

        else:
            error_msg = "The integrity of the database has been affected"

        LOG.warning(f"Fail to add rating: {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Dealing with general exceptions
        error_msg = f"It was not possible to add the rating"
        LOG.warning(error_msg)
        return {"message": error_msg}, 400

   
@app.put(
    rule="/change_rating",
    tags=[RATING_TAG],
    responses={
        "200": PutRating,
        # "400": ErrorSchema,
        # "409": ErrorSchema,
    }
)
def change_rating(form: PutRating):
    """Change the rating for a movie or series

    """
    LOG.info(f"Trying to change the previous rating for {form.rating}")
    session = Session()

    if db_data := session.query(model.Rating).filter(
        model.Rating.audiovisual_id == form.audiovisual_id
    ).one_or_none():
        
        db_data.rating = form.rating
        session.add(db_data)
        session.commit()

        LOG.info(f"The rating has been changed to {form.rating}")
        return {"rating": form.rating}, 200
    
    error_msg = f"There is no movie or series related to {form.audiovisual_id}"
    LOG.warning(f"{error_msg}")
    return {"message": error_msg}, 409


@app.delete(
    rule="/delete_rating", 
    tags=[RATING_TAG],
    responses={
        # "200": EsportistaDeletadoSchema, 
        # "404": ErrorSchema
    }
)
def delete_rating(query: RatingQuery):
    """Delete a movie or series' rating from the collection

    """
    LOG.info(f"Trying to remove the rating related to {query.audiovisual_id}")
    session = Session()

    if session.query(model.Rating).filter(
        model.Rating.audiovisual_id 
        == UUID(unquote(query.audiovisual_id))
    ).delete():
        
        session.commit()
        msg = "Previous rating has been removed"
        LOG.info(f"The rating is no longer on the collection")
        return {"message": msg}, 200
    
    error_msg = f"There is no rating related to {query.audiovisual_id}"
    LOG.warning(f"{error_msg}")
    return {"message": error_msg}, 404