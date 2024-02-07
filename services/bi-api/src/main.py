"""
Main App

Define application runtime and its dependencies:
- Configs
- Routers
- Connections
"""
import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI

from src.config import Config

# Setup
app = FastAPI()
app_config = Config()

# Router
from src.services.v1 import v1_bi_router
app.include_router(v1_bi_router)

@app.get("/")
async def healthcheck():
    return {
        "message": "Hello World",
        "version": "1.0.0"
    }
