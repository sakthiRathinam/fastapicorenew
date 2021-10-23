from src.config.settings import DATABASE_URI, APPS_MODELS
import os
# TORTOISE_ORM = {
#     "connections": {"default": {
#         "engine": "tortoise.backends.asyncpg",
#         "credentials": {
#             "database": os.environ.get('POSTGRES_DBNAME'),
#             "host": os.environ.get('POSTGRES_HOST'),
#             "password": os.environ.get('POSTGRES_PASSWORD'),
#             "port": os.environ.get('POSTGRES_PORT'),
#             "user": os.environ.get('POSTGRES_USER'),
#         },
#     }},
#     "apps": {
#         "models": {
#             "models": APPS_MODELS,
#             "default_connection": "default",
#         }
#     },
#
# }

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URI},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}
# db_config = {
#     "connections": {
#         "default": {
#             "engine": "tortoise.backends.asyncpg",
#             "credentials": {
#                 "database": 'fastapicore',
#                 "host": 'postgresdb',
#                 "password": 'newpassword',
#                 "port": '5432',
#                 "user": 'sakthi',
#             },
#         }
#     },
#     "apps": {
#         "models": {
#             "models": settings.APPS_MODELS,
#             "default_connection": "default",
#         }
#
#     },
#
# }
