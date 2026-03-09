from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import team, login

app = FastAPI(title="Ristosagra API")

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(team.router)
app.include_router(login.router)
