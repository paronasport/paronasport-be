from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username", "password")
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise PydanticCustomError("empty_field", "Il campo non può essere vuoto")
        return v.strip()

class LoginResponse(BaseModel):
    token: str
    expiresIn: int

class User(BaseModel):
    id: str
    username: str
    role: str

    model_config = {"from_attributes": True}