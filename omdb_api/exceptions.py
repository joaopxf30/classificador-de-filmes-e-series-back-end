class LackOfDataException(Exception):
    msg = "A title or IMDb ID must be sent in order to find a movie or series"


class DataNotFoundException(Exception):
    msg = "There is no movie or series on the database based on the search key"


class OMDbApiException(Exception):
    ...
