from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    expiresIn: int

class User(BaseModel):
    id: str
    username: str
    role: str