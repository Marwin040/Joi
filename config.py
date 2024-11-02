from os import getenv

LOAD = getenv("LOAD", "").split()

NO_LOAD = getenv("NO_LOAD", "").split()

TOKEN = getenv("TOKEN", "7343734756:AAHiKuQRQhY60nl-p7OqskcTlhcBvJIyyeg")

MONGO_DB_URL = getenv(
    "MONGO_DB_URL",
    "marwin0985:BEwJvxaADStDLScc@cluster0.oh0nk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

START_IMG_URL = getenv(
    "START_IMG_URL", "https://envs.sh/_IF.jpg"
)
