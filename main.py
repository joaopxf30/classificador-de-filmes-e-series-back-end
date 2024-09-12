from schema import POSTAudiovisual
from app import add_audiovisual, get_audiovisuals

if __name__ == "__main__":
    audiovisual = add_audiovisual(
        POSTAudiovisual.model_validate(
            {
                "IMDbID":None,
                "title":"Central do Brasil",
                "year":None,
            }
        )
    )

    audiovisual = get_audiovisuals()
    print(audiovisual)
