from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
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
            raise PydanticCustomError("invalid_name", "Il nome non può essere vuoto")
        return v.strip()
