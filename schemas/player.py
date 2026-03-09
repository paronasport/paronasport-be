from pydantic import BaseModel, field_validator, model_validator

class PlayerCreate(BaseModel):
    name: str
    surname: str
    ciId: str
    birthDate: str

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Il nome non può essere vuoto")
        return v.strip()
    
    @field_validator("surname")
    def surname_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Il cognome non può essere vuoto")
        return v.strip()

    @field_validator("ciId")
    def ciId_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Il codice identificativo non può essere vuoto")
        return v.strip()
    
    @field_validator("birthDate")
    def birthDate_not_empty(cls, v):
        if not v.strip():
            raise ValueError("La data di nascita non può essere vuota")
        return v.strip()
    
    @field_validator("birthDate")
    def birthDate_format(cls, v):
        try:
            from datetime import datetime
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La data di nascita deve essere nel formato DD/MM/YYYY")
        return v.strip()

class PlayerResponse(BaseModel):
    id: int
    name: str
    surname: str
    ciId: str
    birthDate: str
    teamName: str = ""

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def extract_squad_name(cls, data):
        if hasattr(data, "team") and data.team is not None:
            data.__dict__["teamName"] = data.team.name
        return data