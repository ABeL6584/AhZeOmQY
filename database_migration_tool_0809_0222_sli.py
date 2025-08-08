# 代码生成时间: 2025-08-09 02:22:04
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
import os

# Pydantic model for database migration
class MigrationConfig(BaseModel):
    url: str
    revision: Optional[str] = None
    message: Optional[str] = None
    autogenerate: Optional[bool] = None
   sql: Optional[bool] = None
   tag: Optional[str] = None

# Initialize FastAPI app
app = FastAPI()

# Error handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Database migration endpoint
@app.post("/migrate")
async def migrate_database(config: MigrationConfig):
    try:
        # Set up the alembic config
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("script_location", "migrations")
        alembic_cfg.set_main_option("sqlalchemy.url", config.url)

        # Perform migration
        if config.revision:
            command.upgrade(alembic_cfg, config.revision)
        elif config.autogenerate:
            command.autogenerate(alembic_cfg)
        elif config.tag:
            command.tag(alembic_cfg, config.tag)
        else:
            # Default to stamping the latest revision
            command.upgrade(alembic_cfg, "head")

        # Return success response
        return {"message": "Migration successful"}
    except Exception as e:
        # Handle any unexpected exceptions
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Dependency to handle JSON responses
async def JSONResponse(response_content):
    return JSONResponse(content=response_content)
