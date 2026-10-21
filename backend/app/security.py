from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, subject: str, role: str, token_version: int = 0) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {"sub": subject, "role": role, "ver": token_version, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if not payload.get("sub"):
            raise ValueError("missing subject")
        return payload
    except (JWTError, ValueError) as exc:  # pragma: no cover - behavior enforced by dependency
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
