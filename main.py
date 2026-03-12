from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import psutil
import os
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
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(team.router)
app.include_router(login.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]["msg"]
    return JSONResponse(
        status_code=422,
        content={"detail": error}
    )

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.head("/health")
async def health():
    return {"status": "ok"}

@app.get("/stats")
async def stats():
    process = psutil.Process(os.getpid())
    ram_mb = process.memory_info().rss / 1024 / 1024
    return {"ram_mb": round(ram_mb, 2)}