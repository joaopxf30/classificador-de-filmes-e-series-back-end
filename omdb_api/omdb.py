import logging
import requests
import backoff
from .exceptions import (
    LackOfDataException,
    DataNotFoundException,
    OMDbApiException,
)
from settings import (
    API_OBDM_HOST,
    API_OBDM_KEY,
)

LOG = logging.getLogger()


class OMDbApi:
    def get_audiovisual(
        self,
        imdb_id: str | None,
        title: str | None,
        year: int | None,
    ):
        return self._get_audiovisual(
            params=self._parameters(imdb_id, title, year),
            url=API_OBDM_HOST,
        )

    @backoff.on_exception(
        backoff.constant,
        exception=OMDbApiException,
        max_tries=3,
        interval=5,
        on_backoff=lambda x: LOG.warning(
            "Something went wrong. Let's try one more time!"
        ),
        on_giveup=lambda x: LOG.warning("Time to give up!"),
        raise_on_giveup=False,
    )
    def _get_audiovisual(self, params: dict, url: str):

        if not (params.get("t") or params.get("i")):
            raise LackOfDataException

        response = requests.get(url, params=params)

        response_json = response.json()
        if response_json.get("Response") == "False":
            raise DataNotFoundException
        
        if response.status_code != 200:
            return OMDbApiException

        return response

    @staticmethod
    def _parameters(imdb_id: str | None, title: str | None, year: int | None):
        params = {"apikey": API_OBDM_KEY}
        if imdb_id:
            params.update({"i": imdb_id})
        if title:
            params.update({"t": title})
        if year:
            params.update({"y": year})

        return params
