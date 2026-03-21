from fastapi import APIRouter, Depends
from schemas.login import LoginRequest, LoginResponse
from services.auth_service import AuthService
from dependencies import get_auth_service

router = APIRouter(prefix="/api/login", tags=["login"])

@router.post("/admin", response_model=LoginResponse)
async def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(data)

@router.post("/teams", response_model=LoginResponse)
async def teams_login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.teams_login(data)