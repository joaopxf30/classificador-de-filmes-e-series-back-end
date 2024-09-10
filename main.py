from schema import POSTAudiovisual
from app import add_audiovisual

if __name__ == "__main__":
    audiovisual = add_audiovisual(
        POSTAudiovisual.model_validate(
            {
                "IMDbID":None,
                "title":"Harry Potter",
                "year":None,
            }
        )
    )
