from pydantic import BaseModel, model_validator, field_validator
from .player import PlayerCreate, PlayerResponse

class TeamCreate(BaseModel):
    name: str
    players: list[PlayerCreate]

class TeamResponse(BaseModel):
    id: int
    name: str
    players: list[PlayerResponse]

    model_config = {"from_attributes": True}

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Il nome non può essere vuoto")
        return v.strip()
