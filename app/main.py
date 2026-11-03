
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
        "message": "DevOps CI/CD Pipeline is running!",
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
