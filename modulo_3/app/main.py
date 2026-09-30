from fastapi import FastAPI, Depends
from app.config import Settings, get_settings

app = FastAPI(title="Orders API - Seguridad")


@app.get("/")
def root(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config-info")
def config_info(settings: Settings = Depends(get_settings)):
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
    }