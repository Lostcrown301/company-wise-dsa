from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import companies, topics, questions

app = FastAPI(
    title="DSA Practice Platform API",
    description="Public Company-Wise DSA Practice Platform",
    version="1.0.0",
)

# Parse CORS origins
if isinstance(settings.cors_origins, str):
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
else:
    origins = settings.cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(topics.router)
app.include_router(questions.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}