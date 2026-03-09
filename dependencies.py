from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from database import get_db
from repositories.team_repo import TeamRepo
from repositories.user_repo import UserRepo
from services.team_service import TeamService
from services.auth_service import AuthService
from auth import decode_token
from schemas.login import User

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token non valido")
        return User(id=user_id, username=payload.get("username"), role=payload.get("role")) # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido o scaduto")

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permesso negato")
    return current_user
    
def get_user_repo(db=Depends(get_db)):
    return UserRepo(db)

def get_auth_service(repo=Depends(get_user_repo)):
    return AuthService(repo)

def get_team_repo(db=Depends(get_db)):
    return TeamRepo(db)

def get_team_service(repo=Depends(get_team_repo)):
    return TeamService(repo)