from fastapi import APIRouter, Depends, HTTPException
from services.team_service import TeamService
from schemas.team import TeamCreate, TeamResponse
from schemas.login import User
from dependencies import get_team_service, get_current_user, require_admin
from exceptions import AlreadyExistsException

router = APIRouter(prefix="/api/teams", tags=["team"])

@router.post("/", status_code=201)
async def create_team(team_data: TeamCreate,
                      service: TeamService = Depends(get_team_service),
                      user: User = Depends(get_current_user)):
    try:
        service.create_team(team_data)
    except AlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[TeamResponse])
async def get_teams(service: TeamService = Depends(get_team_service),
                    admin: User = Depends(require_admin)):
    return service.get_teams()