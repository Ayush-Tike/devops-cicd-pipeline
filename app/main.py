
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="DevOps CI/CD Demo",
    description="Automated CI/CD pipeline demonstration",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Version 2 deployed through CI/CD!",
        "application": "CI/CD Demo API",
        "status": "success"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/version")
def version():
    return {
        "version": "1.0.0",
        "environment": "production"
    }
