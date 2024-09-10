class LackOfDataException(Exception):
    msg = "A title or IMDb ID must be sent in order to find a movie or series"


class OMDbApiException(Exception):
    ...