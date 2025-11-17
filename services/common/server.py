"""
Common server utilities for Λ‑Möbius services
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(name: str) -> FastAPI:
    """
    Create a FastAPI application with common configuration
    
    Args:
        name: Service name
        
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=f"Λ‑{name.capitalize()}",
        description=f"Part of Λ‑Möbius Pentastrat AI‑OS",
        version="1.0.0"
    )

    @app.get("/health")
    def health():
        """Health check endpoint"""
        return {"status": "ok", "service": name}

    return app


def run(app: FastAPI, port: int = 8000):
    """
    Run the FastAPI application
    
    Args:
        app: FastAPI application instance
        port: Port to listen on
    """
    logger.info(f"Starting service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
