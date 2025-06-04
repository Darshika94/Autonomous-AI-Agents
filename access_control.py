from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"

def generate_token(role: str, expires_in_minutes: int = 30):
    expiry = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    payload = {
        "role": role,
        "exp": expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded.get("role")
    except JWTError:
        return None

