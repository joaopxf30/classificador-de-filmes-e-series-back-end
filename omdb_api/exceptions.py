class OMDbKnownExcpetion(Exception):
    ...


class OMDbApiException(Exception):
    ...


class LackOfDataException(OMDbKnownExcpetion):
    msg = "A title or IMDb ID must be sent in order to find a movie or series"


class DataNotFoundException(OMDbKnownExcpetion):
    msg = "There is no movie or series on the database based on the search key"

