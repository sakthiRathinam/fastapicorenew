import os
import pathlib
PROJECT_NAME = "FastAPICORE"
SERVER_HOST = os.environ.get("SERVER_HOST")

# Secret key
SECRET_KEY = "5994f0aa99574b68fb9ba9582758eca935ba7ce3"

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAZOR_API_KEY = os.environ.get("RAZOR_API_KEY")
RAZOR_SECRET_KEY = os.environ.get("RAZOR_SECRET_KEY")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

STATIC_ROOT =pathlib.Path.joinpath(BASE_DIR,'static')
MEDIA_ROOT = pathlib.Path.joinpath(BASE_DIR,'media')


API_V1_STR = "/api/v1"

# Token EXPIRES AFTER !% DAYS
ACCESS_TOKEN_EXPIRE_DAYS = 15


# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://192.168.29.12",
    "http://192.168.29.98",
    '*',
    "http://192.168.29.242",
]

DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("POSTGRES_HOST")}:5432/' \
               f'{os.environ.get("POSTGRES_DBNAME")}'

#virtual_mondo_db_host              
# mongodb+srv://sakthi:newpassword@sakthimongo.lesxv.mongodb.net/myFirstDatabase
VIRTUAL_MONGO_URL = f'mongodb+srv://{os.environ.get("VIRTUAL_MONGO_USER")}:' \
            f'{os.environ.get("VIRTUAL_MONGO_PASSWORD")}@' \
            f'{os.environ.get("VIRTUAL_MONGO_HOST")}/'
            
#local mongo_db_host
LOCAL_MONGO_URL = f'mongodb://{os.environ.get("LOCAL_MONGO_USER")}:'\
                f'{os.environ.get("LOCAL_MONGO_PASSWORD")}@'\
                f'{os.environ.get("LOCAL_MONGO_HOST")}:27017/'
            


USERS_OPEN_REGISTRATION = True

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "src/email-templates/html"

# Email
SMTP_TLS = os.environ.get("SMTP_TLS")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")

EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL
EMAIL_TEST_USER = "djwoms@gmail.com"

APPS_MODELS = [
    "src.apps.users.models",
    "src.apps.auth.models",
    "src.apps.prescriptionapp.models",
    "src.apps.razorpay.models",
    "src.apps.dunzo.models",
    "aerich.models",

]
