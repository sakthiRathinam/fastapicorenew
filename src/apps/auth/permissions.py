import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Security,Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN
from src.config import settings

from src.apps.users.models import User
from src.apps.users import service

from .jwt import ALGORITHM
from .schema import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")




async def current_user(token: str):
    # try:
    print(token)
    payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[ALGORITHM])
    print(payload)
    token_data = TokenPayload(**payload)
    # except PyJWTError:
    #     raise HTTPException(
    #         status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    #     )
    user = await service.user_service.get_obj(id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user(current_user: User = Security(current_user)):
    """ Проверка активный юзер или нет """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# async def check_token(token:)
