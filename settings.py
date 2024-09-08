import os
from os import environ
from dotenv import load_dotenv

load_dotenv()

API_OBDM_HOST = os.getenv("API_OBDM_HOST", "http://www.omdbapi.com")


