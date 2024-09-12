import jwt
from jwt.exceptions import InvalidTokenError
from functools import wraps
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.domain.models import Token
from salestrackapifjf.core.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = jwt.decode(kwargs['dependencies'], settings.JWT_SECRET_KEY, settings.ALGORITHM)
        user_id = payload['sub']
        data = kwargs['session'].query(Token).filter_by(user_id=user_id, access_token=kwargs["dependencies"], status=True).first()
        if data:
            return func(kwargs['dependencies'], kwargs['session'])
        else:
            return {"message": "Unauthorized Token"}
    return wrapper


def decodeJWT(jwttoken: str):
    try:
        payload = jwt.decode(jwttoken, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        return payload
    except InvalidTokenError:
        return None
    

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authentication Scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try: 
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload: 
            isTokenValid = True
        return isTokenValid
    

jwt_bearer = JWTBearer()