from datetime import datetime, timedelta
from jose import jwt, JWTError
from .schemas import Token, TokenData

SECRET_KEY = "afc272d9efa4a8a16df8109486cd6a06223ee12fc71e0383a7648f8d743b57db"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 999999

def create_access_token(data:dict):
    to_encode = data.copy()
    expiry = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp":expiry})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_access_token(oauth2_token: str, credential_exception):
    try:
        payload = jwt.decode(oauth2_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenData(email = email)
        return token_data
    except JWTError:
        raise credential_exception