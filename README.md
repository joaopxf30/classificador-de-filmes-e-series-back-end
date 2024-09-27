# Movie and series' catalogue (Back-end)

This project was done for the MVP from the sprint of **Advanced Back-end Development** as part of the Full Stack Development. This app is responsible for searching for movies and series and adding them on a catalogue. It is possible to rate them and it is also possible to check informations from their production. The OMDb API provides the content from the audiovisuals. The present documentation focuses on aspects of the back-end development.


---
## Virtual environment
It is a good practice to work with virtual environments in Python. Open the terminal from a desired path and accordingly to the operational system do the following command:

**WINDOWS**:
```
python -m venv env
```

**OS/LINUX**:
```
python3 -m venv env
```
Now, it is necessary to activate the virtual environment. Therefore, do the following according to the platform:

**WINDOWS**:
```
<path>\env\Scripts\Activate.ps1
```

**POSIX**:
```
source <path>/env/bin/activate
```

The virtual enviroment is set up

## Managing dependencies
All dependencies of the project are available in `requirements.txt`. Do the following in the root of the project in order to install them:

```
pip install -r requirements.txt
```

The dependencies are installed.

## Internal APIs

There are two main entities in this project: **audiovisuals** and **ratings**.

Audiovisuals consist on the content related to the movier os series itself: name, year, actors, directors... Ratings are given by the user to each audiovisual.

There are 3 APIs relating to Audiovisuals:
+ GET -> Show all audiovisuals and their given rating from the database;
+ POST -> Add a new audiovisual into the database (It relates to the external API from OMDb);
+ DELETE -> Remove a previous audiovisual from the database.

There are 3 APIs relating to Ratings:
+ POST -> Add a new rating to a previous movie or series into the database;
+ PUT -> Change a preivous rating on the database;
+ DELETE -> Remove the rating from the database.

The APIs are available when the following command is done in the root of the project:

```
flask run --host 0.0.0.0 --port 5001
```

### Documentation

The internal APIs' documentation is available on http://127.0.0.1:5001/openapi/swagger.

## External API

The audiovisual content comes indeed from the OMDb API. The back-end of the project is responsible for interacting with OMDb. Whenever a POST request is done for an Audiovisual entity, the server performs a GET request to the OMDb API to retrieve the data. For more information about it, check https://www.omdbapi.com.

## Overall considerations

### Programming language

Python 3.11.2 was the chosen programming language.

### Database

The chosen DBMS is SQLite and the interaction between the server and the database is done through SQLAlchemy's ORM.

__
## Run app with Docker

Before proceeding, it is important to have Docker installed.

### Build the image
Open the terminal in the root `.movies-and-series-catalogue-back-end`. The `Dockerfile` and `requirements.txt` are there.
Execute the following command:

```
docker build . -t movies-and-series-catalogue-back-end
```

If everything succeds, an image named `movies-and-series-catalogue-back-end` will be created. To check it, run the following in the same terminal:

```
docker images
````

A similar response should be seen in a good scenario:
```
REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
movies-and-series-catalogue-back-end   latest    7bf0cba0ae33   31 minutes ago   1.19GB
```

#### Details of the image
This image provides a virtualized environment with all the dependencies from the `requirements.txt` and `pyhton:3.11`.


### Run a container from the image
Now, execute the following to create a container from the image:

```
docker run --name msc-back-end -dp 5001:5001 movies-and-series-catalogue-back-end
```

It creates a container named msc-back-end, which binds the port 5001 of the container to the port 5001 of the host.

Whenever it is necessary to stop the container, do the following command:

```
docker stop msc-back-end
```

Now, there is no need to create again another container. To run the same one, just do:

```
docker start msc-back-end
```



