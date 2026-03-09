from fastapi import HTTPException
from repositories.user_repo import UserRepo
from schemas.login import LoginRequest, LoginResponse
from auth import verify_password, create_token
from config import settings

class AuthService:
    def __init__(self, repo: UserRepo):
        self.repo = repo
    
    def login(self, data: LoginRequest) -> LoginResponse:
        user = self.repo.get_user_by_username(data.username)

        if not user or not verify_password(data.password, str(user.hashed_password)):
            raise HTTPException(status_code=401, detail="Credenziali non valide")
        
        token = create_token({"sub": user.id, "username": user.username, "role": user.role})
        return LoginResponse(token=token, expiresIn=settings.token_expire_minutes*60)