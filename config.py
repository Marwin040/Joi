from os import getenv

LOAD = getenv("LOAD", "").split()

NO_LOAD = getenv("NO_LOAD", "").split()

TOKEN = getenv("TOKEN", "7343734756:AAFE6T6wuFeIPSlJfaI6ZVf5E69zsOR-IxI")

MONGO_DB_URL = getenv(
    "MONGO_DB_URL",
    "mongodb+srv://marwin0985:BEwJvxaADStDLScc@cluster0.oh0nk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/fb0a52cab97ca0aa4c523-dda25587b44c6713d4.jpg"
)
