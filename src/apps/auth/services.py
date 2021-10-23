from fastapi import BackgroundTasks
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from typing import Optional
from tortoise.query_utils import Q

from src.config import settings

from src.app.user import schemas, service, models
