# Paronasport Backend
 
REST API backend for managing registration for football tournaments organized by **Paronasport**. It allows the registration of teams and players, with authentication of administrators and data validation.
 
> **Frontend:** [paronasport.netlify.app](https://paronasport.netlify.app)  
> **API (production):** [paronasport-be.onrender.com](https://paronasport-be.onrender.com/), deploy on [Render](https://render.com)
 
---
 
## Tech Stack
 
| Layer | Technology |
|---|---|
| Python | 3.12.3 |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL (Neon — serverless) |
| Validation | Pydantic v2 |
| Authentication | JWT (`python-jose` + `bcrypt`) |
| Deploy | Render |
 
---
 
## Project structure
 
```
paronasport-be/
│
├── main.py              # Entry point: app FastAPI, middleware CORS, routers, exception handlers
├── config.py            # Configuration through pydantic-settings (reads from .env)
├── database.py          # Engine SQLAlchemy and SessionLocal
├── auth.py              # Generation and verification JWT
├── dependencies.py      # Dependency injection (get_db, get_current_user, ...)
├── exceptions.py        # Custom exceptions for the application
│
├── models/              # SQLAlchemy models (database's tables)
├── schemas/             # Pydantic v2 schemas (request/response)
├── repositories/        # Database access (CRUD query)
├── services/            # Business logic
├── routers/             # FastAPI endpoints (team, login)
├── scripts/             # Utility scripts
│
├── alembic/             # Alembic migrations
├── alembic.ini          # Alembic configuration
│
├── requirements.txt
├── .env.example
└── .gitignore
```
---
 
## Local setup
 
### 1. Clone repository
 
```bash
git clone https://github.com/paronasport/paronasport-be.git
cd paronasport-be
```
 
### 2. Create and activate a virtual environment
 
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Configure environment variables
 
Copy the example file and fill in the values:
 
```bash
cp .env.example .env
```
 
```env
DATABASE_URL='postgresql://user:password@host/dbname?sslmode=require'
SECRET_KEY=long-random-secret-key
FRONTEND_URL=http://localhost:5173
TOKEN_EXPIRE_MINUTES=30
```
 
### 5. Run migrations
 
```bash
alembic upgrade head
```
 
### 6. Start the server
 
```bash
uvicorn main:app --reload
```
 
API will be available on 'http://localhost:8000`.  
Interactive documentation (Swagger UI) is accessible at 'http://localhost:8000/docs`.
 
---
 
## API Endpoints
 
### Auth
 
| Metodo | Path | Descrizione |
|---|---|---|
| `POST` | `/login/token` | Login — restituisce un access token JWT |
 
### Team
 
| Metodo | Path | Descrizione |
|---|---|---|
| `GET` | `/teams` | List of all registered teams |
| `POST` | `/teams` | Register a new team with its players |
 
> Endpoints require a valid JWT token in the 'Authorization: Bearer <token>' header.
 
### Utility
 
| Metodo | Path | Descrizione |
|---|---|---|
| `GET` | `/` | Redirect to `/docs` |
| `HEAD` | `/health` | Health check (used by UptimeRobot) |
 
---
 
## Deploy on Render
 
The project is configured to deploy to Render (free tier).
 
**Build command:**
```bash
pip install -r requirements.txt && alembic upgrade head
```
 
**Start command:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
 
Environment variables (`DATABASE_URL`, `SECRET_KEY`, `FRONTEND_URL`, `TOKEN_EXPIRE_MINUTES`) must be configured in the Render panel.
 
> **Note:** Render's free tier puts the service on sleep after 15 minutes of inactivity. To keep it active it is recommended to configure an external monitor (e.g. [UptimeRobot](https://uptimerobot.com) or [Freshping](https://www.freshping.io)) pointing to the '/health' endpoint.
 
---
 
## Database Notes
 
The database is hosted on [Neon](https://neon.tech) (PostgreSQL serverless). The connection string uses Neon's **pooler** ('-pooler' in the hostname) for efficient connection management. SQLAlchemy is configured with 'pool_pre_ping=True' to detect and reconnect any expired connections.