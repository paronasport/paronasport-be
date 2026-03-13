from pydantic import BaseModel, field_validator, model_validator
from pydantic_core import PydanticCustomError
from datetime import date, datetime

class PlayerCreate(BaseModel):
    name: str
    surname: str
    ciId: str
    birthDate: date

    @field_validator("name", "surname", "ciId")
    def not_empty(cls, v):
        if not v.strip():
            raise PydanticCustomError("empty_field", "Il campo non può essere vuoto")
        return v.strip()
    
    @field_validator("birthDate", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v.strip(), "%d/%m/%Y").date()
            except ValueError:
                raise PydanticCustomError("invalid_date", "La data deve essere nel formato DD/MM/YYYY")
        return v

class PlayerResponse(BaseModel):
    id: int
    name: str
    surname: str
    ciId: str
    birthDate: str
    teamName: str = ""

    model_config = {"from_attributes": True}

    @field_validator("birthDate", mode="before")
    def format_date(cls, v):
        if isinstance(v, date):
            return v.strftime("%d/%m/%Y")
        return v

    @model_validator(mode="before")
    @classmethod
    def extract_team_name(cls, data):
        if hasattr(data, "team") and data.team is not None:
            return {**data.__dict__, "teamName": data.team.name}
        return data