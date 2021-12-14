import os
import pathlib
import socketio
PROJECT_NAME = "FastAPICORE"
SERVER_HOST = os.environ.get("SERVER_HOST")
sio = socketio.AsyncClient()
DUNZO_HEADERS = {
    'client-id': 'a61aec7d-50af-4dc0-b933-d09d9d82e320',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkIjp7InJvbGUiOjEwMCwidWlkIjoiYjg5MzhjMjctZGE2Ni00OGQ5LWFmMTctOTRiMjlkODQ0NTZhIn0sIm1lcmNoYW50X3R5cGUiOm51bGwsImNsaWVudF9pZCI6ImE2MWFlYzdkLTUwYWYtNGRjMC1iOTMzLWQwOWQ5ZDgyZTMyMCIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHl0b29sa2l0Lmdvb2dsZWFwaXMuY29tL2dvb2dsZS5pZGVudGl0eS5pZGVudGl0eXRvb2xraXQudjEuSWRlbnRpdHlUb29sa2l0IiwibmFtZSI6InRlc3RfNzUzNzU3MTUyNCIsInV1aWQiOiJiODkzOGMyNy1kYTY2LTQ4ZDktYWYxNy05NGIyOWQ4NDQ1NmEiLCJyb2xlIjoxMDAsImR1bnpvX2tleSI6ImE4NzZjODliLTc2MzktNDljMi05OGI0LTgzNWI4Y2Q0OGUxNCIsImV4cCI6MTc4NTU2NzcwNCwidiI6MCwiaWF0IjoxNjMwMDQ3NzA0LCJzZWNyZXRfa2V5IjoiZDc3MTMwNTEtYWRiMi00NTNiLWE3ODktZjY2YzY3NjJkOWQxIn0.dD1TObR1hxMJjvY8QF5jyj7hXhP9ni_qzykUI6yPCl4',
    'Accept-Language': 'en_US',
    'Content-Type': 'application/json'
}
DUNZO_URL = "https://apis-staging.dunzo.in/api/v2/tasks"
# Secret key
SECRET_KEY = "5994f0aa99574b68fb9ba9582758eca935ba7ce3"

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAZOR_API_KEY = os.environ.get("RAZOR_API_KEY")
RAZOR_SECRET_KEY = os.environ.get("RAZOR_SECRET_KEY")

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

STATIC_ROOT =pathlib.Path.joinpath(BASE_DIR,'static')
MEDIA_ROOT = pathlib.Path.joinpath(BASE_DIR,'media')

MESSAGE_SERVER_KEY = '0bkGBRHsO2MN3D7vKmJ4Trcf1yhIXWA6i5jlnCQYeVPUdqgtzZw23peSmIlNDPZrE0gaQfTcq7sinMhO'

API_V1_STR = "/api/v1"

# Token EXPIRES AFTER !% DAYS
ACCESS_TOKEN_EXPIRE_DAYS = 15

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# GOOGLE_SECRET_KEY = os.environ.get("GOOGLE_SECRET_KEY")
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
testing = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiaSIsImV4cGlyZXMiOiIyMDIxLTEyLTI5In0.neEWBQp1hAHmSEuq52P1wRvR_Qk1yRyZr574gMLMnrs"

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
            
# INVENTORY_MICROSERVICE_HOST = os.environ.get("INVENTORY_HOST")

# MAIN_MICROSERVICE_HOST = os.environ.get("MAIN_HOST")
INVENTORY_MICROSERVICE_HOST = "http://192.168.29.98:8002"
MAIN_MICROSERVICE_HOST = "http://192.168.29.98:8002"
CHAT_MICROSERVICE_HOST = "http://192.168.29.98:9005"


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
