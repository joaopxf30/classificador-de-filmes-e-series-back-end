from omdb_api import OMDBApi

if __name__ == "__main__":
    OMDBApi().get_movie(
        title="Jennie+The+Manner+of+Hell",
        year=2000,
    )