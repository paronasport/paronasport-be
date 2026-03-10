from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import team, login

app = FastAPI(title="Paronasport API")

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url,
                   "http://localhost:3000",
                   "http://localhost:5173",
                   ],
    allow_methods=["GET", "POST", "HEAD"],
    allow_headers=["*"],
)

app.include_router(team.router)
app.include_router(login.router)

@app.head("/health")
async def health():
    return {"status": "ok"}