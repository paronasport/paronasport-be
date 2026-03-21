from fastapi import HTTPException
from repositories.user_repo import UserRepo
from repositories.team_repo import TeamRepo
from schemas.login import LoginRequest, LoginResponse
from auth import verify_password, create_token
from config import settings

class AuthService:
    def __init__(self, user_repo: UserRepo, team_repo: TeamRepo):
        self.user_repo = user_repo
        self.team_repo = team_repo
    
    def login(self, data: LoginRequest) -> LoginResponse:
        user = self.user_repo.get_user_by_username(data.username)

        if not user or not verify_password(data.password, str(user.hashed_password)):
            raise HTTPException(status_code=401, detail="Credenziali non valide")
        
        token = create_token({"sub": user.id, "username": user.username, "role": user.role})
        return LoginResponse(token=token, expiresIn=settings.token_expire_minutes*60)

    def teams_login(self, data: LoginRequest) -> LoginResponse:
        user = self.user_repo.get_user_by_username(data.username)

        if not user or not verify_password(data.password, str(user.hashed_password)):
            raise HTTPException(status_code=401, detail="Credenziali non valide")
        
        team = self.team_repo.get_team_by_name(str(data.username))
        if team:
            raise HTTPException(status_code=401, detail="Squadra già creata")
        
        token = create_token({"sub": user.id, "username": user.username, "role": user.role})
        return LoginResponse(token=token, expiresIn=settings.token_expire_minutes*60)